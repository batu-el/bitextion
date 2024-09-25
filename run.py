# gets the data from data folder
# gets the code from library
# makes computations
# saves the results in res
from lib.data_generation.generate import generate_new_dataset
from lib.simulation.simulate import simulate_conversations
from lib.objective_function.formulate import extract_formulations
from lib.objective_function.score import score_formulations

# Run the function
if __name__ == "__main__":
    # Step 1. Data Generation
    source_dataset_folder = "data/nlp4lp"
    target_dataset_folder = "res/data"
    # generate_new_dataset(source_dataset_folder, target_dataset_folder)
    # Step 2. Simulating Conversations
    source_dataset_folder = "res/data"
    target_dataset_folder = "res/conversations"
    # simulate_conversations(source_dataset_folder , target_dataset_folder)
    # Step 3. Extract Problem Formulations
    source_dataset_folder = "res/conversations"
    target_dataset_folder = "res/formulations"
    # extract_formulations(source_dataset_folder , target_dataset_folder)
    # Step 4. Score Problem Formulations
    source_dataset_folder = "res/formulations"
    target_dataset_folder = "res/scores"
    target_formulation_path = "data/nlp4lp"
    score_formulations(source_dataset_folder , target_dataset_folder, target_formulation_path)
    # Step 5. 