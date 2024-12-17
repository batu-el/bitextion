import os, json, tqdm
from ..utils.utils import check_file_existence
from ..utils.formats import Problem
from ..simulate_user_study.conversation_tree import generate_flat_tree, pick_one_path
from ..simulate_user_study.user import User

def run_simulation(dataset_folder, client, experts, num_levels, branches_per_node):
    problems = [f for f in os.listdir(dataset_folder) if os.path.isdir(os.path.join(dataset_folder, f))]
    
    source_problem_paths = {problem: dataset_folder + '/' + problem + '/' + 'input.json' for problem in problems}
    source_problem_paths = check_file_existence(source_problem_paths)[0]
    problems = list(source_problem_paths.keys())
    target_problem_paths = {problem: dataset_folder + '/' + problem + '/' + 'simulated_conversations.json' for problem in problems}
    
    complete_problems, incomplete_problems = [], []
    
    for problem in tqdm.tqdm(problems[:]):
        try:
            with open(source_problem_paths[problem], "r") as f:
                state = json.load(f)
            detailed_description = state['detailed_description']
            vague_description = state['vague_description']
            user = User(detailed_description, vague_description,  client, persona=None)
            root_conversation = f"User: {vague_description}"

            out = state
            for expert_name in experts:
                flat_tree = generate_flat_tree(user, experts[expert_name], branches_per_node, num_levels, root_conversation)
                out[expert_name] = {str(key): flat_tree[key] for key in flat_tree.keys()} 

            # create the folder if the folder is not present
            os.makedirs(os.path.dirname(target_problem_paths[problem]), exist_ok=True)
            # save it to the file
            with open(target_problem_paths[problem], 'w') as file:
                json.dump(dict(out), file, indent=2)  
            complete_problems.append(problem)
        except:
            if os.path.exists(target_problem_paths[problem]):
                os.remove(target_problem_paths[problem])
                print(f"{target_problem_paths[problem]} has been deleted.")    
            incomplete_problems.append(problem)
    return complete_problems, incomplete_problems