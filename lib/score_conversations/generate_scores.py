import os, json, tqdm
from ..utils.utils import check_file_existence
from ..score_conversations.problem_extraction import extract_problem
from ..score_conversations.problem_score import score_problem

def generate_scores(dataset_folder, expert_names, client):
    problems = [f for f in os.listdir(dataset_folder) if os.path.isdir(os.path.join(dataset_folder, f))]
    
    source_problem_paths = {problem: dataset_folder + '/' + problem + '/' + 'simulated_conversations.json' for problem in problems}
    source_problem_paths = check_file_existence(source_problem_paths)[0]
    problems = list(source_problem_paths.keys())
    target_problem_paths = {problem: dataset_folder + '/' + problem + '/' + 'scored_conversations.json' for problem in problems}
    
    complete_problems, incomplete_problems = [], []

    for problem in tqdm.tqdm(problems[:]):
        try:
            with open(source_problem_paths[problem], "r") as f:
                state = json.load(f)

            out = state
            out["formulation"] = {}
            out["score"] = {}
            for expert_name in expert_names:
                out["formulation"][expert_name] = {}
                out["score"][expert_name] = {}

                for conversation_idx in state[expert_name].keys():
                    curr_conversation = state[expert_name][conversation_idx]
                    pred_problem = extract_problem(curr_conversation, client)
                    curr_score = score_problem(pred_problem, target_parameters=state["target_parameters"], target_objective=state["target_objective"], target_constraints=state["target_constraints"], client=client) 
                    out["formulation"][expert_name][conversation_idx] = pred_problem
                    out["score"][expert_name][conversation_idx] = curr_score
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