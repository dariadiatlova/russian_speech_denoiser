import os
import numpy as np
import shutil
import re


COMMON_VOICE_CLEAN = "/home/dadyatlova_1/dataset/main/common_voice/clean_wav/"
COMMON_VOICE_NOISY = "/home/dadyatlova_1/dataset/main/common_voice/noised_wav/"
COMMON_VOICE_TXT = "/home/dadyatlova_1/dataset/main/common_voice/txt/"

YOUTUBE_CLEAN = "/home/dadyatlova_1/dataset/main/youtube/clean_wav/"
YOUTUBE_NOISY = "/home/dadyatlova_1/dataset/main/youtube/noised_wav/"
YOUTUBE_TXT = "/home/dadyatlova_1/dataset/main/youtube/txt/"

ASR_CLEAN_DIR = "/home/dadyatlova_1/dataset/main/asr/clean"
ASR_NOISY_DIR = "/home/dadyatlova_1/dataset/main/asr/noisy"
ASR_TXT_DIR = "/home/dadyatlova_1/dataset/main/asr/txt"


def __copy(filenames, cv: bool = True):
    CLEAN_DIR = COMMON_VOICE_CLEAN if cv else YOUTUBE_CLEAN
    NOISY_DIR = COMMON_VOICE_NOISY if cv else YOUTUBE_NOISY
    TXT_DIR = COMMON_VOICE_TXT if cv else YOUTUBE_TXT
    prefix = "CV_cv_" if cv else "YouTube_t"

    for filename in filenames:
        shutil.copy(CLEAN_DIR + filename, ASR_CLEAN_DIR + filename)
        shutil.copy(NOISY_DIR + filename, ASR_NOISY_DIR + filename)

        pattern = re.compile(r"\_([\d]+)\_")
        found = pattern.search(filename)
        txt_original_name = prefix + found.group(1) + ".txt"

        pattern = re.compile(r"(.*)\.wav")
        found = pattern.search(filename)
        txt_new_filename = found.group(1) + ".txt"

        shutil.copy(TXT_DIR + txt_original_name, ASR_TXT_DIR + txt_new_filename)


def main(n_files: 1000):
    cv_filenames = next(os.walk(COMMON_VOICE_CLEAN))[2]
    np.random.shuffle(cv_filenames)
    cv_filenames = cv_filenames[: n_files]
    __copy(cv_filenames, cv=True)

    youtube_filenames = next(os.walk(YOUTUBE_CLEAN))[2]
    np.random.shuffle(youtube_filenames)
    youtube_filenames = youtube_filenames[: n_files]
    __copy(youtube_filenames, cv=False)
    print(f"Saved {n_files * 2} to {ASR_CLEAN_DIR}, {ASR_NOISY_DIR} and {ASR_TXT_DIR} directories!")


if __name__ == "__main__":
    main()
