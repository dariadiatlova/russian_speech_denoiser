#!/usr/bin/bash

for f in /home/dadyatlova_1/dataset/open_stt/radio_opus_files/*.opus; do
  filename="${f##*/}"
  filename="${filename%.*}"
  ffmpeg -i "$f" "/home/dadyatlova_1/dataset/open_stt/radio_wav_files/${filename}.wav"; done
