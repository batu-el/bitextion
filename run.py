# gets the data from data folder
# gets the code from library
# makes computations
# saves the results in res
from library.data_generation.generate import generate_new_dataset

# Run the function
if __name__ == "__main__":
    source_dataset_folder = "data/nlp4lp"
    target_dataset_folder = "res"
    generate_new_dataset(source_dataset_folder, target_dataset_folder)