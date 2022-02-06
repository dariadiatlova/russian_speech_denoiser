TRAIN_NOISY_DIR="/home/dadyatlova_1/russian_speech_denoiser/DNS-Challenge/datasets/training_set_jan14_min35_10_40h/noisy_train"
TRAIN_CLEAN_DIR="/home/dadyatlova_1/russian_speech_denoiser/DNS-Challenge/datasets/training_set_jan14_min35_10_40h/clean_train"

VAL_NOISY_DIR="/home/dadyatlova_1/russian_speech_denoiser/DNS-Challenge/datasets/training_set_jan14_min35_10_40h/noisy_val"
VAL_CLEAN_DIR="/home/dadyatlova_1/russian_speech_denoiser/DNS-Challenge/datasets/training_set_jan14_min35_10_40h/clean_val"

TEST_NOISY_DIR="/home/dadyatlova_1/russian_speech_denoiser/DNS-Challenge/datasets/training_set_jan14_min35_10_40h/noisy_test"
TEST_CLEAN_DIR="/home/dadyatlova_1/russian_speech_denoiser/DNS-Challenge/datasets/training_set_jan14_min35_10_40h/clean_test"


declare -a TRAIN_CLEAN_ARRAY=($(ls $TRAIN_CLEAN_DIR))
read -d'\n' TRAIN_CLEAN_ARRAY < <(printf '%s\n' "${TRAIN_CLEAN_ARRAY[@]}"|tac)

declare -a TRAIN_NOISY_ARRAY=($(ls $TRAIN_NOISY_DIR))
read -d'\n' TRAIN_NOISY_ARRAY < <(printf '%s\n' "${TRAIN_NOISY_ARRAY[@]}"|tac)

declare -a VAL_CLEAN_ARRAY=($(ls $VAL_CLEAN_DIR))
read -d'\n' VAL_CLEAN_ARRAY < <(printf '%s\n' "${VAL_CLEAN_ARRAY[@]}"|tac)

declare -a VAL_NOISY_ARRAY=($(ls $VAL_NOISY_DIR))
read -d'\n' VAL_NOISY_ARRAY < <(printf '%s\n' "${VAL_NOISY_ARRAY[@]}"|tac)

declare -a TEST_CLEAN_ARRAY=($(ls $TEST_CLEAN_DIR))
read -d'\n' TEST_CLEAN_ARRAY < <(printf '%s\n' "${TEST_CLEAN_ARRAY[@]}"|tac)

declare -a TEST_NOISY_ARRAY=($(ls $TEST_NOISY_DIR))
read -d'\n' TEST_NOISY_ARRAY < <(printf '%s\n' "${TEST_NOISY_ARRAY[@]}"|tac)

mkdir -p "/home/dadyatlova_1/russian_speech_denoiser/DNS-Challenge/datasets/dtln_6th_feb/noisy_train/"
mkdir -p "/home/dadyatlova_1/russian_speech_denoiser/DNS-Challenge/datasets/dtln_6th_feb/clean_train/"

mkdir -p "/home/dadyatlova_1/russian_speech_denoiser/DNS-Challenge/datasets/dtln_6th_feb/noisy_val/"
mkdir -p "/home/dadyatlova_1/russian_speech_denoiser/DNS-Challenge/datasets/dtln_6th_feb/clean_val/"

mkdir -p "/home/dadyatlova_1/russian_speech_denoiser/DNS-Challenge/datasets/dtln_6th_feb/noisy_test/"
mkdir -p "/home/dadyatlova_1/russian_speech_denoiser/DNS-Challenge/datasets/dtln_6th_feb/clean_test/"

for name in ${TRAIN_CLEAN_ARRAY[@]}; do
  i=${name##*_}
  echo ${name}
  echo ${i}
  cp "${TRAIN_CLEAN_DIR}/${name}" "/home/dadyatlova_1/russian_speech_denoiser/DNS-Challenge/datasets/dtln_6th_feb/clean_train/${i}"
done

for name in ${TRAIN_NOISY_ARRAY[@]}; do
  i=${name##*_}
  cp "${TRAIN_NOISY_DIR}/${name}" "/home/dadyatlova_1/russian_speech_denoiser/DNS-Challenge/datasets/dtln_6th_feb/noisy_train/${i}"
done


for name in ${VAL_CLEAN_ARRAY[@]}; do
  i=${name##*_}
  cp "${VAL_CLEAN_DIR}/${name}" "/home/dadyatlova_1/russian_speech_denoiser/DNS-Challenge/datasets/dtln_6th_feb/clean_val/${i}"
done

for name in ${VAL_NOISY_ARRAY[@]}; do
  i=${name##*_}
  cp "${VAL_NOISY_DIR}/${name}" "/home/dadyatlova_1/russian_speech_denoiser/DNS-Challenge/datasets/dtln_6th_feb/noisy_val/${i}"
done


for name in ${TEST_CLEAN_ARRAY[@]}; do
  i=${name##*_}
  cp "${TEST_CLEAN_DIR}/${name}" "/home/dadyatlova_1/russian_speech_denoiser/DNS-Challenge/datasets/dtln_6th_feb/clean_test/${i}"
done

for name in ${TEST_NOISY_ARRAY[@]}; do
  i=${name##*_}
  cp "${TEST_NOISY_DIR}/${name}" "/home/dadyatlova_1/russian_speech_denoiser/DNS-Challenge/datasets/dtln_6th_feb/noisy_test/${i}"
done


echo "Files were copied successfully"