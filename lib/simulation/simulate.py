import os
import tqdm
import json
from openai import OpenAI
from ..utils.all import load_openai_api_key, check_file_existence
from ..simulation.conversation import generate_conversation

OPENAI_API_KEY = load_openai_api_key()
client = OpenAI(api_key = OPENAI_API_KEY)

def simulate_conversations(source_dataset_folder, target_dataset_folder):
    problems = [f for f in os.listdir(source_dataset_folder) if os.path.isdir(os.path.join(source_dataset_folder, f))]
    source_problem_paths = {problem: os.path.join(source_dataset_folder, problem, 'input.json') for problem in problems}
    source_problem_paths = check_file_existence(source_problem_paths)[0]
    problems = list(source_problem_paths.keys())
    target_problem_paths = {problem: os.path.join(target_dataset_folder, problem, 'input.json') for problem in problems}

    complete_problems = []
    incomplete_problems = []
    
    for problem in tqdm.tqdm(problems):
        try:
            with open(source_problem_paths[problem], "r") as f:
                state = json.load(f)
            original_description = state['original_description']
            vague_description = state['vague_description']
            conversations, questions, responses = generate_conversation(original_description, vague_description)
            output_dict = {"original_description": original_description,
                            "vague_description": vague_description,
                            "conversations": conversations,
                            "questions":questions,
                            "responses":responses,
                            }        
            # create the folder if the folder is not present
            os.makedirs(os.path.dirname(target_problem_paths[problem]), exist_ok=True)
            # save it to the file
            with open(target_problem_paths[problem], 'w') as file:
                json.dump(output_dict, file, indent=2)  
            complete_problems.append(problem)
        except:
            incomplete_problems.append(problem)
        if problem == problems[3]:
            break
    return complete_problems, incomplete_problems