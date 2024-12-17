import json
from ..utils.formats import UserResponse

class User:
    def __init__(self, detailed_description, vague_description,  client, persona=None, binary=True):
        # Add personality to the users
        self.vague_description =  vague_description
        self.detailed_description =  detailed_description
        self.client = client
        if binary:
            self.system_prompt = f"You are a user with the following optimization problem: {self.detailed_description} \n\n You will answer questions based on what is explicitly asked, providing accurate 'Yes' or 'No' answers."
        else:
            self.system_prompt = f"You are a user with the following optimization problem: {self.detailed_description} \n\n You will answer questions based on what is explicitly asked, providing accurate information. The expert will ask questions one by one, and you should provide concise, one-sentence responses. You don't know of which details are most relevant, so you will only share what is directly requested."
        self.persona = persona
        self.response_format = UserResponse

    def generate_response(self, conversation):
        completion = self.client.beta.chat.completions.parse(model="gpt-4o-2024-08-06", messages=[{"role": "system", "content":self.system_prompt},  {"role": "user", "content":conversation}],response_format=self.response_format)
        return json.loads(completion.choices[0].message.content)["response"]