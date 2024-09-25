import os
import tqdm
import json
from openai import OpenAI
from ..utils.all import load_openai_api_key, OptimizationProblem, check_file_existence

OPENAI_API_KEY = load_openai_api_key()
client = OpenAI(api_key = OPENAI_API_KEY)

def formulate_problem(conversation):
    system_prompt = f"Based on the conversation, provide the formulation of this optimization problem."
    user_prompt = f"Conversation: {conversation}"
    completion = client.beta.chat.completions.parse(model="gpt-4o-2024-08-06", 
                                                    messages=[{"role": "system", "content":system_prompt},
                                                                {"role": "user", "content": user_prompt}],
                                                    response_format=OptimizationProblem)
    return json.loads(completion.choices[0].message.content)

def extract_formulations(source_dataset_folder, target_dataset_folder):
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
            conversations = state['conversations']
            formulations = {idx: formulate_problem(conversation) for idx, conversation in enumerate(conversations)}
            state["formulations"] = formulations
            # create the folder if the folder is not present
            os.makedirs(os.path.dirname(target_problem_paths[problem]), exist_ok=True)
            # save it to the file
            with open(target_problem_paths[problem], 'w') as file:
                json.dump(state, file, indent=2)  
            complete_problems.append(problem)
        except:
            incomplete_problems.append(problem)
        if problem == problems[3]:
            break
    return complete_problems, incomplete_problems