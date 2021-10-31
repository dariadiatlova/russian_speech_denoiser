from src.utils.util import get_file_paths
from torch import Tensor
import torchaudio
import librosa

import numpy as np


class CreateNoiseData:
    def __init__(self, config: dict):
            self.config = config
            self.file_paths = get_file_paths(config["noise_directory"])

    def noise_single_audio(self, clean_signal: Tensor):
        noise_signal, sr = torchaudio.load(np.random.choice(self.file_paths))
        if sr != self.config["sample_rate"]:
            noise_signal = librosa.resample(noise_signal, sr, self.config["sample_rate"])
        return noise_signal * self.config["sum_coefficient"] + clean_signal
