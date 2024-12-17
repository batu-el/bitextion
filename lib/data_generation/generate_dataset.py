import os, json, tqdm
from ..utils.utils import check_file_existence
from ..utils.formats import Problem

def generate_dataset(source_dataset_folder, target_dataset_folder, client):
    # Handle file I/O
    problems = [f for f in os.listdir(source_dataset_folder) if os.path.isdir(os.path.join(source_dataset_folder, f))]     # problems in the source dataset
    source_problem_paths = {problem: source_dataset_folder + '/' + problem + '/' + 'input_targets.json' for problem in problems}  # use the input files
    source_problem_paths = check_file_existence(source_problem_paths)[0] # check the existence of the file (some are missing)
    problems = list(source_problem_paths.keys()) # list of problems
    target_problem_paths = {problem: target_dataset_folder + '/' + problem + '/' + 'input.json' for problem in problems} # target problem paths
    
    # Initialize the list for complete and incomplete problems
    complete_problems, incomplete_problems = [], []
    # Generate vague descriptions
    for problem in tqdm.tqdm(problems):
        # Try generation of vague description (we need it because sometimes the API returns an unexpected value)
        try:
            # Load the problem description
            with open(source_problem_paths[problem], "r") as f:
                state = json.load(f)
                problem_description = state['description']
            # Generate the vague description
            system_prompt = "Give a vague single sentence description of the problem. "
            user_prompt = "Problem: " + problem_description
            completion = client.beta.chat.completions.parse(model="gpt-4o-2024-08-06", messages=[{"role": "system", "content":system_prompt}, {"role": "user", "content": user_prompt}], response_format=Problem)
            completion_string =  completion.choices[0].message.content
            vague_description = json.loads(completion_string)["description"]
            output_dict = {"vague_description":vague_description,
                           "detailed_description": state['description'], 
                           "target_objective": state['objective'],
                           "target_constraints":  state['constraints'],
                           "target_parameters": [param["definition"] for param in state['parameters']],
                           }
            # Save the vague description
            os.makedirs(os.path.dirname(target_problem_paths[problem]), exist_ok=True) # create the folder if the folder is not present
            with open(target_problem_paths[problem], 'w') as file:
                json.dump(output_dict, file, indent=2)  
            complete_problems.append(problem)
        # If generation failed, add the problem into the list of incomplete problems
        except:
            incomplete_problems.append(problem)    
    return complete_problems, incomplete_problems