import torch
import torchaudio
import numpy as np
import re

from typing import List, Tuple, Optional
from archive.utils.util import write_wav
from os.path import join

from tqdm import trange, tqdm


def add_noise(wav_audio_file_paths: List[str], noise_samples: Optional[List[str]],
              noise_coefficient: float = 1.0) -> Tuple[List[str], List[torch.Tensor], List[torch.Tensor]]:
    noised_samples = []
    noisy_audio = torchaudio.load(noise_samples[0])[0][0]
    clean_audio_list = []

    for clean_audio in tqdm(wav_audio_file_paths):
        if len(noise_samples) > 1:
            noisy_audio = torchaudio.load(np.random.choice(noise_samples, 1))[0][0]
        speech_clean = torchaudio.load(clean_audio)[0][0]
        clean_audio_list.append(speech_clean)

        if len(speech_clean) > len(noisy_audio):
            n_repetitions = int(np.ceil(len(speech_clean) / len(noisy_audio)))
            noisy_audio = np.concatenate([noisy_audio for _ in range(n_repetitions)])
        noised_speech = speech_clean + (noise_coefficient * noisy_audio[:len(speech_clean)])
        noised_samples.append(noised_speech)

    return wav_audio_file_paths, clean_audio_list, noised_samples


def save_samples_for_debug(origin_file_names: List[str], clean_speech: List[torch.Tensor],
                           noisy_speech: List[torch.Tensor],
                           repository_root_directory: str = "denoiser/dataset/russian_debug") -> None:
    # regex matches filename, i.e. match for "/Users/diat.lov/Data/test/farfield/9df9506dfe899409dbc002e5f66c8e98.wav"
    # is: "9df9506dfe899409dbc002e5f66c8e98"
    pattern = "[^\/]*(?=\.wav)"
    for i in trange((len(origin_file_names))):
        filename = re.search(pattern, origin_file_names[i]).group(0) + ".wav"
        write_wav(join(repository_root_directory, "clean", filename), clean_speech[i])
        write_wav(join(repository_root_directory, "noisy", filename), noisy_speech[i])
