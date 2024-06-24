# ENA (European Nucleotide Archive) RNAseq Quantification Pipeline
A pipeline that given a BioProject ID will download and quantify all FASTQ files using Salmon for analysis. 

### Background
I created this pipeline so that I could easily download and quantify transcriptomic data from the ENA. One of the annoying things I ran into when doing this manually was storage where for a given project you could have to download > 200Gb of files. To deal with this, I set up the logic so that it would download a pair of files at a time, process them, then delete the files before moving on, thereby reducing the overall amount of storage needed at any given time.

### Requirements & Setup
The pipeline is written in Python and makes calls to a Salmon docker container via ```subprocess```. Because of this you'll need the following packages installed:
- docker >= 7.1.0
- requests >= 2.31.0

To ensure Salmon docker container runs correctly locally, I reccomend that you allocate at least 8GB of memory to Docker. Insufficient memory can cause performance issues or failures when building a reference index and quantifying FASTQ files.

### Usage

***Pull Salmon Docker Container & Build Target Transcriptome (Human Only)***   
This only needs to be run once, will pull Salmon docker image, download a human reference transcriptome and build the index
 ```python
from ena_quant import setup_salmon
set_up_salmon()
```

***Download and Quantify FASTQs for a BioProject***
```python
from ena_quant import download_and_quantify_bioproject_fastqs
bioproject_id = "PRJNA494155"
output_dir = "./PRJNA494155_output/"
download_and_quantify_bioproject_fastqs(bioproject_id, output_dir)
```
