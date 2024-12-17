import json
import os

# Load API keys
def load_api_keys(file_path='../secret/keys.json'):
    with open(file_path) as f:
        config = json.load(f)
    return config
# Get subfolders
def get_subfolders(directory):
    return [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
# Check if a file exists
def check_file_existence(file_paths_dict):
    # input: dict of file paths
    # output: dict of existing_files, dict of missing_files
    existing_files = {}
    missing_files = {}
    for key, file_path in file_paths_dict.items():
        if os.path.exists(file_path):
            existing_files[key] = file_path
        else:
            missing_files[key] = file_path
    return existing_files, missing_files