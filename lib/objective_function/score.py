
import os
import tqdm
import json
from openai import OpenAI
from ..utils.all import load_openai_api_key, SimilarityScore, check_file_existence

OPENAI_API_KEY = load_openai_api_key()
client = OpenAI(api_key = OPENAI_API_KEY)

def generate_similarity_score(predicted_problem, original_problem):
    system_prompt = """
    Evaluate the similarity between the predicted problem formulation and the original problem formulation.  
    Score the similarity on a scale of 0 to 5 based on how well the following key components match between the predicted and original problem:
    - **Objective**: Does the predicted problem aim to achieve the same outcome as the original?
    - **Constraints**: Do both problems have the same constraints?
    - **Parameters**: Are the same parameters considered in both problems?
    Ignore the structure, wording, and specific phrasing. Focus only on the core meaning. Give a list of differences for each item: objective, constraints, and parameters. Then, give a similarity score for each item.  

    Scale:
    0: No similarity
    1: Low similarity
    2: Partial similarity
    3: Moderate similarity
    4: High similarity
    5: Near-exact or exact match
    """
    system_prompt = f"Evaluate the similarity between the predicted problem formulation and the original problem formulation. Score this similarity on a scale of 0 to 100, based on how closely the predicted formulation matches the original."
    user_prompt = f"Original Problem Formulation: {original_problem}\nPredicted Problem Formulation: {predicted_problem}"
    completion = client.beta.chat.completions.parse(model="gpt-4o-2024-08-06", 
                                                    messages=[{"role": "system", "content":system_prompt},
                                                                {"role": "user", "content":user_prompt}],
                                                    response_format=SimilarityScore)
    return json.loads(completion.choices[0].message.content)

def score_formulations(source_dataset_folder, target_dataset_folder, target_formulation_path):
    problems = [f for f in os.listdir(source_dataset_folder) if os.path.isdir(os.path.join(source_dataset_folder, f))]
    source_problem_paths = {problem: os.path.join(source_dataset_folder, problem, 'input.json') for problem in problems}
    source_problem_paths = check_file_existence(source_problem_paths)[0]
    problems = list(source_problem_paths.keys())
    target_problem_paths = {problem: os.path.join(target_dataset_folder, problem, 'input.json') for problem in problems}
    target_formulation_paths = {problem: os.path.join(target_formulation_path, problem, 'input_targets.json') for problem in problems}

    complete_problems = []
    incomplete_problems = []
    
    for problem in tqdm.tqdm(problems):
        try:
            with open(source_problem_paths[problem], "r") as f:
                state = json.load(f)
                formulations =state["formulations"]
            with open(target_formulation_paths[problem], "r") as f:
                input_targets = json.load(f)
                target_formulation = {"constraints" : input_targets["constraints"], "objectives" : input_targets["objective"], "parameters" : input_targets["parameters"],}
            
            scores = {idx: generate_similarity_score({key: formulations[idx][key] for key in ['objective', 'constraints', 'parameters']} , target_formulation) for idx in formulations}
            state["scores"] = scores
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