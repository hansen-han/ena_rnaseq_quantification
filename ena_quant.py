import requests
import pandas as pd
import json
import subprocess
import os
import urllib.request
import docker

def is_docker_running():
    # check if the docker daemon is running
    try:
        client = docker.from_env()
        client.ping()
        return True
    except docker.errors.APIError as e:
        return False

def delete_file(file_path):
    try:
        # Check if file exists
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File {file_path} has been deleted.")
        else:
            print(f"File {file_path} does not exist.")
    except Exception as e:
        print(f"Error occurred while trying to delete the file: {e}")

def download_ftp_file(ftp_url, local_directory):
    # Parse the filename from the FTP URL
    filename = os.path.basename(ftp_url)
    
    # Ensure the local directory exists
    if not os.path.exists(local_directory):
        os.makedirs(local_directory)
    
    # Define the local file path
    local_file_path = os.path.join(local_directory, filename)
    
    # Check if the file already exists
    if os.path.exists(local_file_path):
        print(f"File {local_file_path} already exists. Skipping download.")
    else:
        # Download the file
        print(f"Downloading {filename} to {local_file_path}...")
        urllib.request.urlretrieve(ftp_url, local_file_path)
        print(f"Downloaded {filename} to {local_file_path}")

def set_up_salmon():
    # Note: Ensure you have allocated >= 8gb of memory for Docker 

    if not is_docker_running():
        raise RuntimeError("Docker daemon is not running, please start the Docker service.")

    # Download Salmon Docker Image
    try:
        # Execute docker pull command
        subprocess.run(['docker', 'pull', 'combinelab/salmon:latest'], check=True)
        print("Docker image 'combinelab/salmon:latest' pulled successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to pull Docker image: {e}")

    # Download Human Reference Transcriptome
    url = "ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_39/gencode.v39.transcripts.fa.gz"
    filename = "gencode.v39.transcripts.fa.gz"

    try:
        print("Downloading target transcriptome (human)")
        # Download the file
        urllib.request.urlretrieve(url, filename)
        print(f"File '{filename}' downloaded successfully.")
    except Exception as e:
        print(f"Failed to download file: {e}")

    
    # Build Index

    # Get the current working directory
    cwd = os.getcwd()

    # Define the Docker command
    command = [
        "docker", "run", "--rm",
        "-v", f"{cwd}:/workdir",
        "-w", "/workdir",
        "combinelab/salmon:latest",
        "salmon", "index",
        "-t", "gencode.v39.transcripts.fa",
        "--gencode", 
        "-i", "gencode_index_2"
    ]

    # Execute the command
    result = subprocess.run(command, capture_output=True, text=True)

def get_project_samples_data(bio_project_id):
    try:
        r = requests.get("https://www.ebi.ac.uk/ena/portal/api/filereport?result=read_run&accession={bio_project_id}&limit=1000&format=json&fields=study_accession,secondary_study_accession,sample_accession,secondary_sample_accession,experiment_accession,run_accession,submission_accession,tax_id,scientific_name,instrument_platform,instrument_model,library_name,nominal_length,library_layout,library_strategy,library_source,library_selection,read_count,base_count,center_name,first_public,last_updated,experiment_title,study_title,study_alias,experiment_alias,run_alias,fastq_bytes,fastq_md5,fastq_ftp,fastq_aspera,fastq_galaxy,submitted_bytes,submitted_md5,submitted_ftp,submitted_aspera,submitted_galaxy,submitted_format,sra_bytes,sra_md5,sra_ftp,sra_aspera,sra_galaxy,sample_alias,broker_name,sample_title,nominal_sdev,first_created,bam_ftp,bam_bytes,bam_md5".format(bio_project_id = bio_project_id))
        response_dict = json.loads(r.text)
        return response_dict
    except Exception as e:
        print("Error fetching project sample data:", e)
        raise RuntimeError()

def download_and_quantify_bioproject_fastqs(project_id):
    project_sample_data = get_project_samples_data(project_id)
    
    # download FASTQ files
    local_directory = './downloaded_files'

    for sample in project_sample_data:
        link_pair = sample['fastq_ftp']
        sample_name = sample
        files = link_pair.split(";")
        for file in files:
            download_ftp_file(file, local_directory)

    # quantify FASTQ files using salmon




