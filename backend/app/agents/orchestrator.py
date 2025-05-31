from dotenv import load_dotenv
import openai
from openai import OpenAI
import os
import json

from app.schemas.build_schema import build_duckdb_schema

load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

async def orchestratorAgent(input: str) -> str:
        
    db_path = "dataset/analytics.duckdb"
    
    schema = build_duckdb_schema(db_path)
    
    system_message = (
        "You are an expert data analyst at valuating user questions, answering them and giving instructions to an sql agent, that fetches a database."
    )
    user_message = """
You are an expert data analyst at valuating user questions, answering them and giving instructions to an sql agent, that fetches a database.

Instructions:
- THE CURRENT USER QUESTION IS THE LAST MESSAGE IN THE MESSAGE ARRAY. USE THIS AS THE USER QUESTION. PREVIOUS MESSAGES ARE CONTEXT FOR YOU
- Use the context, they newest question might refer to previous questions the user asked
- Evaluate if a user question makes sense in terms of a database data analysis question
- Create a json output that is either an answer to the user input (last message in the Input: ) or an instruction to an sql agent
- If the user question is way too broad / unclear / not relevant to the schema you have, answer the user and ask for clarification
- if the user question is good, create an instruction for an sql agent to create an sql command, based on the schema you have

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
Output format example when you are answering the user directly
{{
    "answer": "Could you specify what you... (or something similar)"
}}

Other:
- Don't wrap the output in a code block
- Be polite to the user
- Be friendly to the user
- Remember that your are a 180iq data analyst and ask good short clarifying questions to the user if needed
- Do not give vague instructions to the sql agent only very very specific orders (in natural language)
- If the user uses ambigious terms like best/worst/very good or similar that can be interpreted in many ways: Always ask the user for more detail and tell what was vague and how they should format the question
""".format(input, schema)

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, temperature=0
    )
    
    assistant_reply = response.choices[0].message.content
    
    result = json.loads(assistant_reply)
    if "answer" in result:
        return result["answer"]
    if "instruction" in result:
        print(result["instruction"])

    
    