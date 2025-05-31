from app.agents.sql_agent import sql_agent
from app.agents.analyst_agent import analyst_agent

from dotenv import load_dotenv
import os
import openai

load_dotenv()  # Load environment variables from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai.api_key)


def main():
    user_question = "give me the graph of total sales by country"
    user_question = "What is the average value of an order fore each customer segment over the past 100 year?"
    # user_question = "For each product category, how much was sold this year compared to last year? Show the difference and percentage change."
    user_question = "What is the average order value for each customer segment in the last 3 months?"
    user_question = "How many sales representatives are there in each country, and what is the average sales amount?"
    user_question = (
        " What are  the top 5 biggest order ever recorded? Plot it with a chart"
    )
    user_question = "Plot biggest orders by id"
    user_question = "Plot timeseries of number of orders in year 2013 for each country for each month of the year. "
    db_path = "dataset/analytics.duckdb"
    sql, result = sql_agent(db_path, client, user_question)
    print(f"Generated SQL: \n{sql}")
    print("Result:")
    if isinstance(result, str):
        print(result)
    else:
        print(result.to_string(index=False))
    messages = analyst_agent(client, result, user_question)
    print(messages)


if __name__ == "__main__":
    main()
