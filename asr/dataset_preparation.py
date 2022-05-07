import os
import numpy as np
import shutil
import re
from tqdm import tqdm


COMMON_VOICE_CLEAN = "/home/dadyatlova_1/dataset/main/no_reverb_50h/test_clean"
COMMON_VOICE_TXT = "/home/dadyatlova_1/dataset/main/common_voice/no_reverb_txt"
ASR_TXT_DIR = "/home/dadyatlova_1/dataset/main/no_reverb_50h/test_txt"


def __copy(filenames):

    for filename in tqdm(filenames):

        pattern = re.compile(r"(.*)\.wav")
        found = pattern.search(filename)
        txt_original_filename = f"{COMMON_VOICE_TXT}/{found.group(1)}.txt"
        txt_new_filename = f"{ASR_TXT_DIR}/{found.group(1)}.txt"

        shutil.copy(txt_original_filename, txt_new_filename)


def main():
    cv_filenames = next(os.walk(COMMON_VOICE_CLEAN))[2]
    print("Common voice files are read.")
    np.random.shuffle(cv_filenames)
    __copy(cv_filenames)

    print(f"Saved {len(cv_filenames)} transcripts to {ASR_TXT_DIR} directories!")


if __name__ == "__main__":
    main()
