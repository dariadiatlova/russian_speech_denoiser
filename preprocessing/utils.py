import torch
import numpy as np
import re
import librosa

from typing import Tuple, List

from tqdm import tqdm
from os.path import join

from archive.utils.util import write_wav


def rename_opus_files_to_wav(file_paths, start_dir_name_to_replicate: str,
                             root_path_for_new_audio: str) -> Tuple[List[str], List[str]]:

    # regex matches a part of filepath that should be replicated
    # i.e. start_dir_name_to_replicate = "test"
    # path = "/Users/user/test/farfield/9df9506dfe899409dbc002e5f66c8e98.opus"
    # match = "test/farfield/9df9506dfe899409dbc002e5f66c8e98"
    pattern = start_dir_name_to_replicate + ".*(?=\.opus)"
    wav_file_paths = []
    opus_file_paths = []
    for path in tqdm(file_paths):
        try:
            filename = re.search(pattern, path).group(0)
            wav_file_paths.append(join(root_path_for_new_audio, filename + ".wav"))
            opus_file_paths.append(path)
        except AttributeError:
            # skip all non .opus files
            continue
    return opus_file_paths, wav_file_paths


def read_opus_files(audio_paths: List[str], target_sr: int = 16_000) -> List[List[float]]:
    audio_tensors = []
    for path in tqdm(audio_paths):
        wav, sr = librosa.load(path, res_type='kaiser_fast')
        if sr != target_sr:
            wav = librosa.resample(wav, sr, target_sr)
        wav = wav.squeeze()
        audio_tensors.append(wav)
    return audio_tensors


def convert_opus_to_wav(audio_list: List[np.ndarray], file_paths: np.ndarray) -> None:
    for audio, path in tqdm(zip(audio_list, file_paths)):
        write_wav(path, audio)
