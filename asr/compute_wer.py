import os
import re

import numpy as np

from typing import Iterable, Dict
from omegaconf import OmegaConf
from tqdm import tqdm

from asr import ASR_ROOT_PATH

CONFIG_PATH = f"{ASR_ROOT_PATH}/conf/wer_config.yaml"


def levenshtein_distance_matrix(a: Iterable, b: Iterable) -> np.ndarray:
    """Matrix implementation of Levenshtein distance

    :param a: Iterable
    :param b: Iterable
    :return distance matrix: np.ndarray
    """
    a = ['#'] + list(a)
    b = ['#'] + list(b)

    d = np.zeros((len(a), len(b)), dtype=int)

    d[0, :] = np.arange(len(b))
    d[:, 0] = np.arange(len(a))

    for i in range(1, d.shape[0]):
        for j in range(1, d.shape[1]):
            cost = 1
            if a[i] == b[j]:
                cost = 0
            insertion = d[i][j - 1] + 1
            delition = d[i - 1][j] + 1
            substitution = d[i - 1][j - 1] + cost

            d[i, j] = min(insertion, delition, substitution)

    return d


def __edit_distance(a: Iterable, b: Iterable) -> int:
    return levenshtein_distance_matrix(a, b)[-1, -1]


def main(args: Dict) -> None:
    edit_distances = []
    target_transcripts = args["true_transcription_dir_path"]
    asr_transcripts = args["transcription_dir_path"]
    filenames = next(os.walk(target_transcripts))[2]

    for filename in tqdm(filenames):
        asr_filename = f"{asr_transcripts}/{filename}"
        try:
            with open(f"{target_transcripts}/{filename}") as f:
                a = f.readlines()

            # demucs enhanced files have different filename
            if args["enhanced"]:
                pattern = re.compile(r"(.*)\.wav")
                found = pattern.search(filename)
                asr_filename = found.group(1) + "_enhanced.wav"

            with open(asr_filename) as f:
                b = f.readlines()

            if a is not None and b is not None:
                edit_distances.append(__edit_distance(a, b))
        except FileNotFoundError:
            print(f"{asr_filename} doesn't exist :(")
    print(f"WER: {np.mean(edit_distances)}")


if __name__ == "__main__":
    config = OmegaConf.load(CONFIG_PATH)
    config = OmegaConf.to_container(config, resolve=True)
    main(config)
