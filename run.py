# gets the data from data folder
# gets the code from library
# makes computations
# saves the results in res
from library.data_generation.generate import generate_new_dataset
from library.simulation.simulate import simulate_conversations
from library.objecive_function.formulate import formulate_problems
from library.objecive_function.score import score_formulations

# Run the function
if __name__ == "__main__":
    # Step 1. Data Generation
    source_dataset_folder = "data/nlp4lp"
    target_dataset_folder = "res/data"
    generate_new_dataset(source_dataset_folder, target_dataset_folder)
    # Step 2. Simulating Conversations
    source_dataset_folder = "res/data"
    target_dataset_folder = "res/conversations"
    simulate_conversations(source_dataset_folder , target_dataset_folder)
    # Step 3. Scoring Conversations

