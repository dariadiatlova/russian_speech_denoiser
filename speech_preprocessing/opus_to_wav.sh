#!/bin/bash

opus_files_directory=$1
wav_files_directory=$2

# write to array all files with a .opus extansion
FILES=$(find $opus_files_directory -type f -name "*.opus")

# naive implementation
#for f in $FILES; do
#  filename="${f##*/}"
#  filename="${filename%.*}"
#  ffmpeg -i "$f" "${wav_files_directory}/${filename}.wav"; done

# multiprocess implementation

opus_to_wav() {

  opus_files_directory=$1
  wav_files_directory=$2
  f=$3

  filename="${f##*/}"
  filename="${filename%.*}"
  # converts opus into wav
  ffmpeg -i "$f" "$wav_files_directory/${filename}.wav";
}

# make a constrain on max number of processes to use
max_num_processes=$(ulimit -u)
limiting_factor=4
num_processes=$((max_num_processes/limiting_factor))


for f in $FILES; do
  ((i=i%num_processes)); ((i++==0)) && wait
  opus_to_wav "$opus_files_directory" "$wav_files_directory" "$f" &
  done
