# Denoiser for Russian speech

This repository consists of implemented demoisers' forks: [DTLN](https://github.com/breizhn/DTLN) and 
[Demucs](https://github.com/facebookresearch/denoiser), a fork of [DNS](https://github.com/microsoft/DNS-Challenge) 
repository which scripts were used as a base for creating 
noised datasets with russian speech and additional supportive scripts for dataset prepartion. 

Bellow are the steps used for finetuning DTLN-denoiser on russian speech which are needed because as the experiments showed both denoisers perform without finetuning poorly.


## Datasets:
For creating noise dataset we used 3 types of noise from [Demand collection](https://zenodo.org/record/1227121#.YjrfYxBBy3K):
- [CAR](https://zenodo.org/record/1227121/files/TCAR_16k.zip?download=1)
- [KITCHEN](https://zenodo.org/record/1227121/files/DKITCHEN_16k.zip?download=1)
- [PARK](https://zenodo.org/record/1227121/files/NPARK_16k.zip?download=1)

As of russian sppech, we used radio and youtube domain from [open-stt](https://github.com/snakers4/open_stt). 
Audio and trascripts can be dowloaded via `wget` from 

    https://azureopendatastorage.blob.core.windows.net/openstt/ru_open_stt_opus/ 
    
with adding the following suffixes to the link above: 
- `archives/radio_2.tar.gz` for radio speech;
- `archives/public_youtube700.tar.gz` for youtube speech.
