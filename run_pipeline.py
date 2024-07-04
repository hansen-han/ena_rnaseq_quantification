import sys
from ena_pipeline import download_and_quantify_bioproject_fastqs

def main():
    if len(sys.argv) != 2:
        print("Usage: python run_pipeline.py <BioProject ID>")
        sys.exit(1)

    project_id = sys.argv[1]
    print(f"Running Pipeline for Project: {project_id}")
    download_and_quantify_bioproject_fastqs(project_id)

if __name__ == "__main__":
    main()