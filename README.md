# ENA (European Nucleotide Archive) Quantification Pipeline
A pipeline that given a BioProject ID will download and quantify all FASTQ files using Salmon for analysis. 

### Background
I created this pipeline so that I could easily download and quantify transcriptomic data from the ENA. One of the annoying things I ran into when doing this manually was storage where for a given project you could have to download > 200Gb of files. To deal with this, I set up the logic so that it would download a pair of files at a time, process them, then delete the files before moving on, which reduced the overall amount of storage needed.
