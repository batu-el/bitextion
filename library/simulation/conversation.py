from ..simulation.agents import expert, user

def generate_conversation(ground_truth_problem_description, vague_problem_description):
    conversations = {}
    questions = {}
    responses = {}

    conversation = f"User: {vague_problem_description}\n"
    conversations[0] = conversation

    for turn in range(1,11):
        expert_question = expert(conversation_history=conversation)["question"]
        conversation += f"Expert: {expert_question}\n"
        user_response = user(conversation_history=conversation, ground_truth_problem_description=ground_truth_problem_description)["response"]
        conversation += f"User: {user_response}\n"
        conversations[turn] = conversation
        questions[turn] = expert_question
        responses[turn] = user_response
    return conversations, questions, responses