import json
import os
from pydantic import BaseModel

### Loading API Keys
def load_api_key(api_key_name, file_path='././secret.json', ):
    try:
        with open(file_path, 'r') as file:
            secrets = json.load(file)
            return secrets.get(api_key_name)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: {file_path} is not a valid JSON file.")
        return None
def load_openai_api_key():
    return load_api_key("OPENAI_API_KEY")
def load_together_api_key():
    return load_api_key("TOGETHER_API_KEY")
def load_wandb_api_key():
    return load_api_key("WANDB_API_KEY")

### Checking and accessing subfolders
def check_file_existence(file_paths_dict):
    existing_files = {}
    non_existing_files = {}
    for key, file_path in file_paths_dict.items():
        if os.path.exists(file_path):
            existing_files[key] = file_path
        else:
            non_existing_files[key] = file_path
    return existing_files, non_existing_files
def get_subfolders(directory):
    return [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

### JSONs for API return type
class Problem(BaseModel):
    description: str
class UserResponse(BaseModel):
    response: str
class ExpertQuestion(BaseModel):
    question: str
class OptimizationProblem(BaseModel):
    objective: str
    constraints: list[str]
    parameters: list[str]