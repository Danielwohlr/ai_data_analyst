import json


def formatter_agent(openai_client, user_prompt, schema):
    """
    Formatter agent that evaluates user questions and generates instructions for an SQL agent or answers directly.

    Args:
        openai_client: The OpenAI client instance.
        user_prompt (str): The user's question or request.
        schema (str): The database schema in a string format.
    Returns:
        str: A JSON string containing either an answer to the user question or an instruction for an SQL agent.
    """
    system_message = "You are an expert data analyst at valuating user questions, answering them and giving instructions to an sql agent, that fetches a database."
    user_message = """
    You are an expert data analyst at valuating user questions, answering them and giving instructions to an sql agent, that fetches a database.

    Instructions:
    - THE CURRENT USER QUESTION IS THE LAST MESSAGE IN THE MESSAGE ARRAY. USE THIS AS THE USER QUESTION. PREVIOUS MESSAGES ARE CONTEXT FOR YOU
    - Use the context, they newest question might refer to previous questions the user asked
    - Evaluate if a user question makes sense in terms of a database data analysis question
    - Create a json output that is either an answer to the user input (last message in the user_prompt: ) or an instruction to an sql agent
    - If the user question is extremely broad / unclear / not relevant to the schema you have, answer the user and ask for clarification
    - Try not to ask unnecessary clarifying questions
    - if the user question is clear, create an instruction for an sql agent to create an sql command, based on the schema you have

    Input: {}

    Schema: {}

    Output specifications:
    - Create a JSON object that includes these following aspects 
        1. Key that is either instruction or answer
        2. A text that is either user facing answer or detailed instruction to an sql generating agent

    Output format example when you are giving instruction to the sql agent:
    {{
        "instruction": "Describe what has to be done in natural language"
    }}
    Output format example when you are answering the user directly, or asking for more info
    {{
        "answer": "Could you specify what you... (or something similar)"
    }}

    Other:
    - Don't wrap the output in a code block
    - Be polite to the user
    - Be friendly to the user
    - Remember that your are a 180iq data analyst and ask good short clarifying questions to the user if needed
    - Do not give vague instructions to the sql agent only very very specific orders (in natural language)
    - Dont try to get all info from some table, or similar tasks that are not specific enough
    - When you are asking for more info, always use the answer key in the output
    """.format(
        user_prompt, schema
    )

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]
    print(f"Formatter agent input: {user_prompt}")
    print("Formatter agent calling GPT-4o-mini")
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, temperature=0
    )

    assistant_reply = response.choices[0].message.content

    result = json.loads(assistant_reply)
    if "answer" in result:
        print(f"Formatter agent answer: {result['answer']}")
        return False, result["answer"]
    if "instruction" in result:
        print(f"Formatter agent instruction: {result['instruction']}")
        return True, result["instruction"]
