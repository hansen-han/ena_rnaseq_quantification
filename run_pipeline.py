import sys
from ena_pipeline import download_and_quantify_bioproject_fastqs

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_pipeline.py <BioProject IDs>")
        sys.exit(1)
    
    # run for each argument
    project_ids = sys.argv[1:]
    for project_id in project_ids:
        try:
            print(f"Running Pipeline for Project: {project_id}")
            download_and_quantify_bioproject_fastqs(project_id)
        except Exception as e:
            print("Failure running project:", project_id)
            print("Error:", e)

if __name__ == "__main__":
    main()