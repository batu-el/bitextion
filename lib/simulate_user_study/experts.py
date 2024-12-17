import json
from ..utils.formats import ExpertQuestion, OptimizationProblem

class Expert:
    def __init__(self, client):
        self.client = client
        self.system_prompt = f"You are an expert in solving optimization problems. Your goal is to uncover key information about the parameters, constraints, and objective of a partially disclosed optimization problem by asking insightful, targeted questions. The user has the relevant information but does not know which details are relevant. You should ask one concise question to extract a yes/no responses from the user."
    def generate_response(self, conversation):
        completion = self.client.beta.chat.completions.parse(model="gpt-4o-2024-08-06", messages=[{"role": "system", "content":self.system_prompt},  {"role": "user", "content":conversation}],response_format=ExpertQuestion)
        return json.loads(completion.choices[0].message.content)["question"]

class Expert_8b:
    def __init__(self, client):
        self.client = client
        self.system_prompt = f"You are an expert in solving optimization problems. Your goal is to uncover key information about the parameters, constraints, and objective of a partially disclosed optimization problem by asking insightful, targeted questions. The user has the relevant information but does not know which details are relevant. You should ask one concise question to extract a yes/no responses from the user."
    def generate_response(self, conversation):
        completion = self.client.chat.completions.create(model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", messages=[{"role": "system", "content":self.system_prompt},{"role": "user", "content":conversation}], response_format={"type": "json_object", "schema": ExpertQuestion.model_json_schema(),})
        return json.loads(completion.choices[0].message.content)["question"]

class Expert_BiTextion:
    def __init__(self, client):
        self.client = client
        self.response_format = ExpertQuestion
        self.problem_prediction_system_prompt = (
            "You are an expert in solving optimization problems. Your task is to predict a detailed optimization problem based on information from a partially disclosed problem and the accompanying conversation. Analyze the given context carefully and provide a comprehensive and plausible problem description that aligns with the provided details.")
        self.bisecting_question_system_prompt = (
            "You are an expert in solving optimization problems. Your goal is to uncover key details about the parameters, constraints, and objectives of a partially disclosed optimization problem by asking precise, targeted questions. The user has relevant information but may not know which details are critical. Formulate one concise yes/no question designed to divide the candidate problem descriptions into two distinct groups, where the answer is 'yes' for half of the descriptions and 'no' for the other half.")
    def sample_problems(self, conversation, num_samples=6):
        candidate_problems = {}
        for sample_idx in range(num_samples):
            completion = self.client.beta.chat.completions.parse(model="gpt-4o-2024-08-06", messages=[{"role": "system", "content":self.problem_prediction_system_prompt},  {"role": "user", "content":conversation}], response_format=OptimizationProblem, temperature=0.8)
            predicted_problem = json.loads(completion.choices[0].message.content)
            candidate_problems[sample_idx] = predicted_problem
        return candidate_problems
    def formulate_question(self, candidate_problems):
        input = f"Candidate Problems: {candidate_problems}"
        completion = self.client.beta.chat.completions.parse(model="gpt-4o-2024-08-06", messages=[{"role": "system", "content":self.bisecting_question_system_prompt},  {"role": "user", "content":input}],response_format=ExpertQuestion, temperature=0.8)
        return json.loads(completion.choices[0].message.content)["question"]
    def generate_response(self, conversation):
        candidate_problems = self.sample_problems(conversation)
        bisecting_question = self.formulate_question(candidate_problems)
        return bisecting_question

class Expert_8b_BiTextion:
    def __init__(self, client):
        self.client = client
        self.response_format = ExpertQuestion
        self.problem_prediction_system_prompt = (
            "You are an expert in solving optimization problems. Your task is to predict a detailed optimization problem based on information from a partially disclosed problem and the accompanying conversation. Analyze the given context carefully and provide a comprehensive and plausible problem description that aligns with the provided details.")
        self.bisecting_question_system_prompt = (
            "You are an expert in solving optimization problems. Your goal is to uncover key details about the parameters, constraints, and objectives of a partially disclosed optimization problem by asking precise, targeted questions. The user has relevant information but may not know which details are critical. Formulate one concise yes/no question designed to divide the candidate problem descriptions into two distinct groups, where the answer is 'yes' for half of the descriptions and 'no' for the other half.")
    def sample_problems(self, conversation, num_samples=6):
        candidate_problems = {}
        for sample_idx in range(num_samples):
            completion = self.client.chat.completions.create(model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", messages=[{"role": "system", "content":self.problem_prediction_system_prompt},  {"role": "user", "content":conversation}], response_format={"type": "json_object", "schema": OptimizationProblem.model_json_schema(),}, temperature=0.8)
            predicted_problem = json.loads(completion.choices[0].message.content)
            candidate_problems[sample_idx] = predicted_problem
        return candidate_problems
    def formulate_question(self, candidate_problems):
        input = f"Candidate Problems: {candidate_problems}"
        completion = self.client.chat.completions.create(model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", messages=[{"role": "system", "content":self.bisecting_question_system_prompt},  {"role": "user", "content":input}],response_format={"type": "json_object", "schema": ExpertQuestion.model_json_schema(),}, temperature=0.8)
        return json.loads(completion.choices[0].message.content)["question"]
    def generate_response(self, conversation):
        candidate_problems = self.sample_problems(conversation)
        bisecting_question = self.formulate_question(candidate_problems)
        return bisecting_question