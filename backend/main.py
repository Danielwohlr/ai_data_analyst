from app.agents.sql_agent import answer_user_query

from dotenv import load_dotenv
import os
import openai

load_dotenv()  # Load environment variables from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai.api_key)

if __name__ == "__main__":
    user_question = "give me the total sales by territory"
    db_path = "dataset/analytics.duckdb"
    sql, result = answer_user_query(db_path, client, user_question)
    print(f"Generated SQL: \n{sql}")
    print("Result:")
    if isinstance(result, str):
        print(result)
    else:
        print(result.to_string(index=False))
