import os
import tqdm
import json
from openai import OpenAI
from ..utils.all import load_openai_api_key, check_file_existence, Problem

OPENAI_API_KEY = load_openai_api_key()
client = OpenAI(api_key = OPENAI_API_KEY)
print(client)

def generate_new_dataset(source_dataset_folder, target_dataset_folder):
    problems = [f for f in os.listdir(source_dataset_folder) if os.path.isdir(os.path.join(source_dataset_folder, f))]
    source_problem_paths = {problem: os.path.join(source_dataset_folder, problem, 'input.json') for problem in problems}
    source_problem_paths = check_file_existence(source_problem_paths)[0]
    problems = list(source_problem_paths.keys())
    target_problem_paths = {problem: os.path.join(target_dataset_folder, problem, 'input.json') for problem in problems}

    complete_problems = []
    incomplete_problems = []

    for problem in tqdm.tqdm(problems):
        try:
            # get original description
            with open(source_problem_paths[problem], "r") as f:
                state = json.load(f)
                original_problem_description = state['description']
            system_prompt =  "Give a vague single sentence description of the problem. "
            user_prompt = "Problem: " + original_problem_description
            completion = client.beta.chat.completions.parse(model="gpt-4o-2024-08-06", 
                                                            messages=[{"role": "system", "content":system_prompt},
                                                                        {"role": "user", "content": user_prompt}],
                                                            response_format=Problem)
            completion_string =  completion.choices[0].message.content
            completion_dict = json.loads(completion_string)
            output_dict = {"original_description": original_problem_description, "vague_description":completion_dict["description"]}
            # create the folder if the folder is not present
            os.makedirs(os.path.dirname(target_problem_paths[problem]), exist_ok=True)
            # save it to the file
            with open(target_problem_paths[problem], 'w') as file:
                json.dump(output_dict, file, indent=2)  
            complete_problems.append(problem)
        except:
            incomplete_problems.append(problem)
    print(target_problem_paths)

    return complete_problems, incomplete_problems