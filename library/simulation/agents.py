import json
from openai import OpenAI
from together import Together
from ..utils.all import load_openai_api_key, load_together_api_key, UserResponse, ExpertQuestion

OPENAI_API_KEY = load_openai_api_key()
client = OpenAI(api_key = OPENAI_API_KEY)
TOGETHER_API_KEY = load_together_api_key()
client_together = Together(api_key= TOGETHER_API_KEY)
### GPT 4o
def generate_response_gpt4o(agent_script, conversation_history, response_format):
    completion = client.beta.chat.completions.parse(model="gpt-4o-2024-08-06", 
                                                    messages=[{"role": "system", "content":agent_script},
                                                                {"role": "user", "content":conversation_history}],
                                                    response_format=response_format)
    return json.loads(completion.choices[0].message.content)
### Llama 3.1 8B
def generate_response_llama(agent_script, conversation_history, response_format):
    completion = client_together.chat.completions.create(model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                                                        messages=[{"role": "system", "content":agent_script},{"role": "user", "content":conversation_history}],
                                                        response_format={"type": "json_object", "schema": response_format.model_json_schema(),})
    return json.loads(completion.choices[0].message.content)
### User Agent
def user(conversation_history, ground_truth_problem_description):
    user_agent_script = f"You are a user with an optimization problem to solve, as described by: {ground_truth_problem_description}. However, you cannot fully disclose the problem at the start. You may only answer questions based on what is explicitly asked, providing minimal but accurate information. The expert will ask questions one by one, and you should provide concise, one-sentence responses. You are unaware of which details are most relevant, so you will only share what is directly requested."
    return generate_response_gpt4o(user_agent_script, conversation_history, UserResponse)
### Expert Agent
def expert(conversation_history):
    expert_agent_script = f"You are an expert in solving optimization problems. Your goal is to uncover key information about an undisclosed problem by asking insightful, targeted questions. You need to find out things like what they’re trying to achieve, any rules they have to follow, what they can change, and any specific numbers or limits involved. The other agent has this information but does not know which details are relevant. You may ask questions one by one to extract concise, one-sentence responses from them."
    return generate_response_llama(expert_agent_script, conversation_history, ExpertQuestion)