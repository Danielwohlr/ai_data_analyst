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
    - THE USER QUESTION IS THE LAST ITEM IN THE Input LIST. IT IS NOT A JSON OBJECT BUT A STRING. OTHER ITEMS THAT ARE WRAPPED IN JSON OBJECTS ARE PREVIOUS MESSAGES AND ARE JUST CONTEXT.
    - The "content" for role "user" refers to user questions and the "content" for role "assistant" refers to previous assistant answers
    - Use the context for understanding the user question, the question might refer to them.
    - Evaluate if a user question makes sense in terms of a database data analysis question
    - Create a json output that is either an answer to the user input (last string in the list specified in the Input: ) or an instruction to an sql agent
    - If the user question is extremely broad / unclear / not relevant to the schema at all, answer the user and ask for clarification
    - Try not to ask unnecessary clarifying questions
    - if the user question is clear, create an instruction for an sql agent to create an sql command, based on the schema you have

    Input: {}

    Schema: {}

    Output specifications:
    - Create a JSON object that includes these following aspects 
        1. Key that is either instruction or answer
        2. A text that is either a user facing answer or clear and simple instruction to an sql generating agent, to execute the user question

    Output format example when you are giving instruction to the sql agent:
    {{
        "instruction": "Describe what has to be done in natural language to the sql agent"
    }}
    Output format example when you are answering the user directly, or asking for more info
    {{
        "answer": "A polite question to the user"
    }}

    Other:
    - Don't wrap the output in a code block
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
