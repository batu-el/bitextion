
import json
from ..utils.formats import OptimizationProblemParameters, OptimizationProblemObjective, OptimizationProblemConstraints

def extract_parameters(conversation, client):
    system_prompt = f"Based on the conversation, give the parameters of this optimization problem."
    user_prompt = f"Conversation: {conversation}"
    completion = client.beta.chat.completions.parse(model="gpt-4o-2024-08-06", messages=[{"role": "system", "content":system_prompt},{"role": "user", "content": user_prompt}], response_format=OptimizationProblemParameters)
    return json.loads(completion.choices[0].message.content)
def extract_objective(conversation, client):
    system_prompt = f"Based on the conversation, give the objective of discussed optimization problem."
    user_prompt = f"Conversation: {conversation}"
    completion = client.beta.chat.completions.parse(model="gpt-4o-2024-08-06",  messages=[{"role": "system", "content":system_prompt}, {"role": "user", "content": user_prompt}], response_format=OptimizationProblemObjective)
    return json.loads(completion.choices[0].message.content)
def extract_constraints(conversation, client):
    system_prompt = f"Based on the conversation, give the constraints of this optimization problem."
    user_prompt = f"Conversation: {conversation}"
    completion = client.beta.chat.completions.parse(model="gpt-4o-2024-08-06", messages=[{"role": "system", "content":system_prompt}, {"role": "user", "content": user_prompt}], response_format=OptimizationProblemConstraints)
    return json.loads(completion.choices[0].message.content)
def extract_problem(conversation, client):
    return {"pred_parameters":extract_parameters(conversation, client) , 
            "pred_objective": extract_objective(conversation, client), 
            "pred_constraints": extract_constraints(conversation, client)}
