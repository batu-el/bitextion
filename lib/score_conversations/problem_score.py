import json
from ..utils.formats import SimilarityScore

def score_parameter_similarity(pred_parameters, target_parameters, client):
    system_prompt = """
    Evaluate the similarity between the predicted parameters and the target parameters.  
    Ignore the structure, wording, and specific phrasing. Focus only on the core meaning. 
    Score the similarity on a scale of 0 to 5 based on how well the predicted parameters and target parameters match:

    Scale:
    0: No similarity
    1: Low similarity
    2: Partial similarity
    3: Moderate similarity
    4: High similarity
    5: Near-exact or exact match
    """
    user_prompt = f"Predicted Parameters: {pred_parameters}\nTarget Parameters: {target_parameters}"
    completion = client.beta.chat.completions.parse(model="gpt-4o-2024-08-06",messages=[{"role": "system", "content":system_prompt},{"role": "user", "content":user_prompt}], response_format=SimilarityScore)
    return json.loads(completion.choices[0].message.content)["similarity_score"]

def score_objective_similarity(pred_objective, target_objective, client):
    system_prompt = """
    Evaluate the similarity between the predicted objective and the target objective.  
    Ignore the structure, wording, and specific phrasing. Focus only on the core meaning. 
    Score the similarity on a scale of 0 to 5 based on how well the predicted objective and target objective match:

    Scale:
    0: No similarity
    1: Low similarity
    2: Partial similarity
    3: Moderate similarity
    4: High similarity
    5: Near-exact or exact match
    """
    user_prompt = f"Predicted Objective: {pred_objective}\nTarget Objective: {target_objective}"
    completion = client.beta.chat.completions.parse(model="gpt-4o-2024-08-06",messages=[{"role": "system", "content":system_prompt},{"role": "user", "content":user_prompt}], response_format=SimilarityScore)
    return json.loads(completion.choices[0].message.content)["similarity_score"]

def score_constraint_similarity(pred_constraints, target_constraints, client):
    system_prompt = """
    Evaluate the similarity between the predicted constraints and the target constraints.  
    Ignore the structure, wording, and specific phrasing. Focus only on the core meaning. 
    Score the similarity on a scale of 0 to 5 based on how well the predicted constraints and target constraints match:

    Scale:
    0: No similarity
    1: Low similarity
    2: Partial similarity
    3: Moderate similarity
    4: High similarity
    5: Near-exact or exact match
    """
    user_prompt = f"Predicted Constraints: {pred_constraints}\nTarget Constraints: {target_constraints}"
    completion = client.beta.chat.completions.parse(model="gpt-4o-2024-08-06",messages=[{"role": "system", "content":system_prompt},{"role": "user", "content":user_prompt}], response_format=SimilarityScore)
    return json.loads(completion.choices[0].message.content)["similarity_score"]

def score_problem(pred_problem, target_parameters, target_objective, target_constraints, client):
    pred_parameters = pred_problem['pred_parameters']
    parameter_similarity_score = score_parameter_similarity(pred_parameters, target_parameters, client)
    pred_objective = pred_problem['pred_objective']
    objective_similarity_score = score_objective_similarity(pred_objective, target_objective, client)
    pred_constraints = pred_problem['pred_constraints']
    constraint_similarity_score = score_constraint_similarity(pred_constraints, target_constraints, client)
    similarity_score = {"p_score":parameter_similarity_score, "o_score":objective_similarity_score, "c_score":constraint_similarity_score,}
    return similarity_score