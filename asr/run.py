import os

from asrecognition import ASREngine
from pathlib import Path
from omegaconf import OmegaConf

from asr import ASR_ROOT_PATH

CONFIG_PATH = f"{ASR_ROOT_PATH}/conf/asr_config.yaml"


class ASR:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        # create folder to store transcription files
        Path(self.transcription_dir_path).mkdir(parents=True, exist_ok=True)
        # initialize asr model from pretrained
        self.asr = ASREngine(self.language)
        # collect all paths to wav files for transcription
        self._collect_wav_paths()

    def _collect_wav_paths(self):
        self.wav_paths = []
        for dirpath, _, filenames in os.walk(self.wav_dir_path):
            for f in filenames:
                self.wav_paths.append(os.path.abspath(os.path.join(dirpath, f)))

    def _write_transcriptions_to_txt(self, transcriptions):
        for res in transcriptions:
            name = res["path"].split('/')[-1].split('.')[0]
            text = res["transcription"]
            with open(f'{self.transcription_dir_path}/{name}.txt', 'w') as f:
                f.write(text)

    def transcribe(self):
        transcriptions = self.asr.transcribe(self.wav_paths)
        self._write_transcriptions_to_txt(transcriptions)


if __name__ == "__main__":
    config = OmegaConf.load(CONFIG_PATH)
    config = OmegaConf.to_container(config, resolve=True)
    asr = ASR(**config)
    asr.transcribe()
