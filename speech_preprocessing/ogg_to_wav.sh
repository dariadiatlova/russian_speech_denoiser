#!/bin/bash

ogg_files_directory=$1
wav_files_directory=$2

# write to array all files with a .ogg extansion
FILES=$(find $ogg_files_directory -type f -name "*.ogg")

# multiprocess implementation

ogg_to_wav() {

  ogg_files_directory=$1
  wav_files_directory=$2
  f=$3

  filename="${f##*/}"
  filename="${filename%.*}"
  # converts ogg into wav
  ffmpeg -i "$f" "$wav_files_directory/${filename}.wav";
}

# make a constrain on max number of processes to use
max_num_processes=$(ulimit -u)
limiting_factor=4
num_processes=$((max_num_processes/limiting_factor))

for f in $FILES; do
  ((i=i%num_processes)); ((i++==0)) && wait
  ogg_to_wav "$ogg_files_directory" "$wav_files_directory" "$f" &
  done
