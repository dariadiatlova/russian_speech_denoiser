#!/bin/bash

clean_data_directory=$1
noise_data_directory=$1

mirror="https://azureopendatastorage.blob.core.windows.net/openstt/ru_open_stt_opus"

# load clean speech
cd clean_data_directory
youtube_data="{$mirror}/archives/public_youtube700.tar.gz"

curl youtube_data | tar -xz

# load noise
cd noise_data_directory

wget https://zenodo.org/record/1227121/files/TCAR_16k.zip?download=1
unzip . TCAR_16k.zip?download=1
rm -r TCAR_16k.zip?download=1

wget https://zenodo.org/record/1227121/files/DKITCHEN_16k.zip?download=1
unzip . DKITCHEN_16k.zip?download=1
rm -r DKITCHEN_16k.zip?download=1

wget https://zenodo.org/record/1227121/files/NPARK_16k.zip?download=1
unzip . NPARK_16k.zip?download=1
rm -r NPARK_16k.zip?download=1
