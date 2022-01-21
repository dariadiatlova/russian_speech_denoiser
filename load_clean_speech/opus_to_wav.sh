#!/usr/bin/bash

# for f in /home/dadyatlova_1/dataset/open_stt/radio_opus_files/*.opus; do
#  filename="${f##*/}"
#  filename="${filename%.*}"
#  ffmpeg -i "$f" "/home/dadyatlova_1/dataset/open_stt/radio_wav_files/${filename}.wav"; done

# multiprocess implementation
opus_to_wav() {

  opus_files_directory=$1
  wav_files_directory=$2
  f=$3

  filename="${f##*/}"
  filename="${filename%.*}"
  ffmpeg -i "$f" "$wav_files_directory/${filename}.wav";

# make a constrain on max number of processes to use
max_num_processes=$(ulimit -u)
limiting_factor=4
num_processes=$((max_num_processes/limiting_factor))


opus_files_directory=$1
wav_files_directory=$2

for f in "$opus_files_directory/*.opus"; do
  ((i=i%num_processes)); ((i++==0)) && wait
  opus_to_wav "$opus_files_directory" "$wav_files_directory" "$f" &
  done