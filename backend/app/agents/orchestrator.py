import os

from dotenv import load_dotenv
from openai import OpenAI

from app.schemas.build_schema import build_duckdb_schema
from app.agents.sql_agent import sql_agent
from app.agents.analyst_agent import analyst_agent, format_analyst_result_with_markdown
from app.agents.formatter_agent import formatter_agent

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
db_path = os.getenv(
    "DUCKDB_DATABASE_PATH",
)
client = OpenAI(api_key=api_key)


async def orchestratorAgent(user_prompt: str):

    print(f"Connecting to DuckDB at: {db_path}")

    schema = build_duckdb_schema(db_path)
    format_ok, format_output = formatter_agent(
        openai_client=client, schema=schema, user_prompt=user_prompt
    )
    if not format_ok:
        # formatter thinks the question is not good enough
        return {
            "role": "assistant",
            "content": format_output,  # Use result directly since it's already a string
        }

    else:
        print(format_output)
        # formatter thinks the question is good enough, so we can call the sql agent with the original user prompt
        sql, df = sql_agent(
            db_path=db_path, openai_client=client, user_query=format_output
        )
        if isinstance(df, str):
            return {
                "answer": "SQL generation failed.",
                "charts": [],
                "error": df,
            }

        analysis_result = analyst_agent(
            openai_client=client, result_df=df, user_prompt=user_prompt, sql_query=sql
        )
        formatted_analysis = format_analyst_result_with_markdown(analysis_result, sql)
        # TODO return also sql and df
        return formatted_analysis
