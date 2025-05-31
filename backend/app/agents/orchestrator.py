import os

from dotenv import load_dotenv
from openai import OpenAI

from app.schemas.build_schema import build_duckdb_schema
from app.agents.sql_agent import sql_agent
from app.agents.analyst_agent import analyst_agent
from app.agents.formatter_agent import formatter_agent

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
db_path = os.getenv(
    "DUCKDB_DATABASE_PATH",
)
client = OpenAI(api_key=api_key)


async def orchestratorAgent(user_prompt: str):

    schema = build_duckdb_schema(db_path)
    format_ok, format_output = formatter_agent(client, schema, user_prompt)
    if not format_ok:
        # formatter thinks the question is not good enough
        return {
            "role": "assistant",
            "content": format_output,  # Use result directly since it's already a string
        }

    else:
        # formatter thinks the question is good enough, so we can call the sql agent with the original user prompt
        sql, df = sql_agent(db_path, client, user_prompt)
        analysis_result = analyst_agent(client, df, user_prompt)
        # TODO return also sql and df
        return analysis_result
