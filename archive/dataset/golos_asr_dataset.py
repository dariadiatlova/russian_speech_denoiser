import os
import json_lines
import librosa
import torch
from torch.utils.data import Dataset
import lmdb
import io
import numpy as np
from tqdm import tqdm

# to ignore PySoundFile failed. Trying audioread instead. https://github.com/librosa/librosa/issues/1015
import warnings
warnings.filterwarnings("ignore")


class SpeechDataset(Dataset):
    SAMPLE_RATE = 16000

    def __init__(self, json_file_name: str, root_prefix: str):
        self.use_lmdb = None
        self.lmdb_env = None
        self.root_prefix = root_prefix
        self.audio_filepath = []
        self.text = []

        with open(os.path.join(self.root_prefix, json_file_name), 'rb') as f:
            for item in json_lines.reader(f):
                self.audio_filepath.append(item["audio_filepath"])
                self.text.append(item["text"])

    def create_lmdb(self, map_size: int = 9e12, dataset_size: int = None):
        if not dataset_size:
            dataset_size = self.__len__()

        # if os.path.exists("golos.lmdb"):
        #     shutil.rmtree("golos.lmdb")

        with lmdb.open("golos.lmdb", map_size=map_size) as env:

            with tqdm(total=dataset_size) as pbar:
                for i in range(dataset_size):
                    instance = self._getitem(i)
                    with env.begin(write=True) as txn:
                        txn.put(f"{i}_wav".encode('UTF-8'), instance["wav"].numpy())
                        txn.put(f"{i}_text".encode('UTF-8'), instance["text"].encode())

                    pbar.update(1)

        self.use_lmdb = True
        self.lmdb_env = lmdb.open("golos.lmdb", max_readers=32, readonly=True, lock=False, meminit=False)

    def _getitem(self, index: int):
        text = self.text[index]
        path = os.path.join(self.root_prefix, self.audio_filepath[index])
        wav, sr = librosa.load(path, res_type='kaiser_fast')

        if sr != self.SAMPLE_RATE:
            wav = librosa.resample(wav, sr, self.SAMPLE_RATE)

        wav = wav.squeeze()

        instance = {
            'path': path,
            'wav': torch.FloatTensor(wav),
            'text': text
        }

        return instance

    def __getitem__(self, index: int):

        if self.use_lmdb:
            with self.lmdb_env.begin(write=False) as txn:
                wav = txn.get(f"{index}_wav".encode("UTF-8"))
                wav = torch.from_numpy(np.frombuffer(io.BytesIO(wav).getvalue(), dtype=np.float32))

                text = txn.get(f"{index}_text".encode("UTF-8"))
                text = text.decode('UTF-8')

                instance = {
                    "wav": wav,
                    "text": text
                }
            return instance

        return self._getitem(index)

    def __len__(self):
        return len(self.audio_filepath)
