import logging
import os
import json_lines
import librosa
import torch
import torchaudio
from torch.utils.data import Dataset
import lmdb
import io
import numpy as np
from tqdm import tqdm
from typing import Tuple, Optional

# to ignore PySoundFile failed. Trying audioread instead. https://github.com/librosa/librosa/issues/1015
import warnings

from src.dataset.text_encoder import BaseTextEncoder
from src.utils.parse_config import ConfigParser

warnings.filterwarnings("ignore")

logger = logging.getLogger(__name__)


class SpeechDataset(Dataset):
    SAMPLE_RATE = 16000

    def __init__(self, config):

        self.config_parser = config

        self.lmdb_map_size: int = self.config_parser["data"]["train"]["datasets"][0]["map_size"]
        self.dataset_size: int = self.config_parser["data"]["train"]["datasets"][0]["dataset_size"]
        self.max_audio_len = self.config_parser["data"]["train"]["datasets"][0]["max_audio_length"]
        self.use_lmdb = self.config_parser["data"]["train"]["datasets"][0]["lmdb"]
        self.root_prefix = self.config_parser["data"]["train"]["datasets"][0]["dataset_directory"]

        self.wave_augment = self.config_parser["augmentations"]["wave"]
        self.spec_augment = self.config_parser["augmentations"]["spectrogram"]

        self.lmdb_env = None
        self.byte_array_shape: Optional[Tuple[int]] = None
        self.audio_filepath = []
        self.text = []
        self.duration = []
        self.idx = []

        path = os.path.join(self.root_prefix, self.config_parser["data"]["train"]["datasets"][0]["json_filename"])
        with open(path, 'rb') as f:
            for item in json_lines.reader(f):
                # add to dataset only non empty audio
                if len(item["text"].strip()) > 0 and item["duration"] < self.max_audio_len:
                    self.audio_filepath.append(item["audio_filepath"])
                    self.text.append(item["text"])
                    self.duration.append(item["duration"])
                    self.idx.append(item["id"])

        self._random_index()
        self.text_encoder = BaseTextEncoder(self.config_parser["tokenizer"], self.text)
        logger.info(f"Dataset size: {len(self.text)}.")

    def _random_index(self):
        if self.dataset_size:
            current_dataset_size = len(self.text)
            if current_dataset_size > self.dataset_size:
                idx = np.random.choice(range(current_dataset_size), self.dataset_size)
                self.audio_filepath = np.array(self.audio_filepath)[idx]
                self.text = np.array(self.text)[idx]
                self.duration = np.array(self.duration)[idx]
                self.idx = np.array(self.idx)[idx]
            else:
                logger.info(
                    f"Dataset size{self.dataset_size} greater that number of samples in the dataset after truncation: "
                    f"{current_dataset_size}")

    def _create_lmdb(self):
        if not self.dataset_size:
            self.dataset_size = self.__len__()

        with lmdb.open("golos.lmdb", map_size=self.lmdb_map_size) as env:

            with tqdm(total=self.dataset_size) as pbar:
                for i in range(self.dataset_size):
                    instance = self._getitem(i)
                    self.byte_array_shape = instance["spectrogram"].numpy().shape

                    with env.begin(write=True) as txn:

                        txn.put(f"{i}_wav".encode("UTF-8"), instance["wav"].numpy())
                        txn.put(f"{i}_spectrogram".encode("UTF-8"), instance["spectrogram"].numpy().tobytes())
                        txn.put(f"{i}_text".encode("UTF-8"), instance["text"].encode())
                        txn.put(f"{i}_text_encoded".encode("UTF-8"), instance["text_encoded"].numpy())
                        txn.put(f"{i}_path".encode("UTF-8"), instance["path"].encode())
                        txn.put(f"{i}_duration".encode("UTF-8"), instance["duration"].to_bytes(2, 'big'))
                        txn.put(f"{i}_id".encode("UTF-8"), instance["id"].encode())

                    pbar.update(1)

        self.use_lmdb = True
        self.lmdb_env = lmdb.open("golos.lmdb", max_readers=32, readonly=True, lock=False, meminit=False)

    def process_wave(self, audio_tensor_wave: torch.Tensor):
        with torch.no_grad():

            # TODO: add wave augmentation
            if self.wave_augment:
                audio_tensor_wave = self.wave_augment(audio_tensor_wave)
            wave2spec = self.config_parser.init_obj(
                self.config_parser["preprocessing"]["spectrogram"],
                torchaudio.transforms,
            )
            audio_tensor_spec = wave2spec(audio_tensor_wave)

            # TODO: add spectrogram augmentation
            if self.spec_augment:
                audio_tensor_spec = self.spec_augment(audio_tensor_spec)
            return audio_tensor_wave, audio_tensor_spec

    def _getitem(self, index: int):
        path = os.path.join(self.root_prefix, self.audio_filepath[index])
        wav, sr = librosa.load(path, res_type='kaiser_fast')

        if sr != self.SAMPLE_RATE:
            wav = librosa.resample(wav, sr, self.SAMPLE_RATE)

        wav = wav.squeeze()
        audio_tensor_wave, audio_tensor_spec = self.process_wave(torch.FloatTensor(wav))

        instance = {
            "path": path,
            "wav": audio_tensor_wave,
            "spectrogram": audio_tensor_spec,
            "text": self.text[index],
            "text_encoded": self.text_encoder.encode(self.text[index]),
            "duration": int(self.duration[index]),
            "id": self.idx[index],
        }

        return instance

    def __getitem__(self, index: int):
        if self.use_lmdb:
            self._create_lmdb()

            with self.lmdb_env.begin(write=False) as txn:
                wav = txn.get(f"{index}_wav".encode("UTF-8"))
                wav = torch.from_numpy(np.frombuffer(io.BytesIO(wav).getvalue(), dtype=np.float32))

                spectrogram = txn.get(f"{index}_spectrogram".encode("UTF-8"))
                spectrogram = torch.from_numpy(np.frombuffer(io.BytesIO(spectrogram).getvalue(), dtype=np.float32))

                text = txn.get(f"{index}_text".encode("UTF-8"))
                text = text.decode('UTF-8')

                text_encoded = txn.get(f"{index}_text_encoded".encode("UTF-8"))
                text_encoded = torch.from_numpy(np.frombuffer(io.BytesIO(text_encoded).getvalue(), dtype=np.float32))

                path = txn.get(f"{index}_path".encode("UTF-8"))
                path = path.decode("UTF-8")

                duration = txn.get(f"{index}_duration".encode("UTF-8"))
                duration = int.from_bytes(io.BytesIO(duration).getvalue(), byteorder='big')

                idx = txn.get(f"{index}_id".encode("UTF-8"))
                idx = idx.decode("UTF-8")

                instance = {
                    "wav": wav,
                    "spectrogram": spectrogram.reshape(self.byte_array_shape[0], -1),
                    "text": text,
                    "text_encoded": text_encoded,
                    "path": path,
                    "duration": duration,
                    "id": idx,
                }
            return instance

        return self._getitem(index)

    def __len__(self):
        return len(self.audio_filepath)


if __name__ == "__main__":
    config_parser = ConfigParser.get_default_configs()
    dataset = SpeechDataset(config_parser)

    item_sample = dataset[0]
    print(item_sample)
