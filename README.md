# Denoiser for Russian speech 

## Preview

This repository consists of implemented demoisers' forks: [DTLN](https://github.com/breizhn/DTLN) and 
[Demucs](https://github.com/facebookresearch/denoiser), a fork of [DNS](https://github.com/microsoft/DNS-Challenge) 
repository which scripts were used as a base for creating 
noised datasets with russian speech and additional supportive scripts for dataset prepartion. 

Bellow are the steps used for finetuning DTLN-denoiser on russian speech which are needed because as the experiments showed both denoisers perform without finetuning poorly.


## Dataset Overview

For model robustness we train denoiser on 2 datasets: [`Open-stt YouTube speech`](https://github.com/snakers4/open_stt) and 
[`Common Voice Version 3.0`](https://commonvoice.mozilla.org/ru/datasets). 
We generate in total `100 hours` (40h of noised wavs and 10h clean speech for each dataset). 

For creating noised dataset we used 3 types of noise from [Demand collection](https://zenodo.org/record/1227121#.YjrfYxBBy3K):
- [CAR](https://zenodo.org/record/1227121/files/TCAR_16k.zip?download=1)
- [KITCHEN](https://zenodo.org/record/1227121/files/DKITCHEN_16k.zip?download=1)
- [PARK](https://zenodo.org/record/1227121/files/NPARK_16k.zip?download=1)

For proper quality we will add reverb to our clean audio dataset, please load rirs provided in DNS Challange: 

   - [RIR26](https://www.openslr.org/resources/26/sim_rir_16k.zip)
   
   - [RIR28](https://www.openslr.org/resources/28/rirs_noises.zip)
   
   - [RIR_table_simple.csv](DNS-Challange/datasets/RIR_table_simple.csv)

## Data downloading scripts

1. Noise, Reverberation and YouTube speech:

Run [download.sh](speech_preprocessing/download.sh) script with two arguments: `<absolute_path_to_clean_speech_directory>` `<absolute_path_to_noise_directory>` 

#### Note:
Use `tar -xvf <downloaded_archive_name.tar.gz>` to unpack downloaded files. Due to the server-errors files can be partly downloaded but will be opened correctly.
    
    
    
2. Mozilla Common voice Version 3.0:

- select [`Common Voice Version 3.0`](https://commonvoice.mozilla.org/ru/datasets), enter your email, click right mouse bottun `copy url adress` and run [`download_mozilla.sh`](speech_preprocessing/download_mozilla.sh) script from the root of cloned repository with an argumet (`copied url adress`).

 
## Create noised audio files

1. Configure [youtube_noisyspeech_synthesizer.cfg](https://github.com/dariadiatlova/DNS-Challenge/blob/master/noisy_speech_synthesis/configs/youtube_noisyspeech_synthesizer.cfg) and run [youtube_noisyspeech_synthesizer.py](https://github.com/dariadiatlova/DNS-Challenge/blob/master/noisy_speech_synthesis/configs/youtube_noisyspeech_synthesizer.py).

2. Configure [cv_noisyspeech_synthesizer.cfg](https://github.com/dariadiatlova/DNS-Challenge/blob/master/noisy_speech_synthesis/configs/cv_noisyspeech_synthesizer.cfg) and run [cvnoisyspeech_synthesizer.py](https://github.com/dariadiatlova/DNS-Challenge/blob/master/noisy_speech_synthesis/configs/cv_noisyspeech_synthesizer.py).


The basic idea of the script:

- choose 6 or less random audio files from your clean speech folder;

- stack choosen audio files padded with zeros to create audios of fixed length (provided in transcript);

- stack transcripts corresponded to the choosen audio files, so you can run ASR and commpute WER;

- pick random folder from downloaded noise-types;

- pick random SNR level from the range you provided in a config;

- generate a mixture of noise and clean audio, considering choosen SNR-level.


Note: the are 2 cheet-hardcoded places in the script:

- we use 6 audiofiles as audio files with the clean speech are about 2 sec and the target length of our audio files is 15 seconds.

- there's a `TCAR` noise type that sounds much quiter then the other noise types, so we substract 20 from randomly choosen `SNR` level if use this noise type.




    
