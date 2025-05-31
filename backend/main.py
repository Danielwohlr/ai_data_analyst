from app.agents.sql_agent import answer_user_query
from app.agents.analyst_agent import run_analyst_agent, normalize_analyst_output

import json
from dotenv import load_dotenv
import os
import openai

load_dotenv()  # Load environment variables from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai.api_key)

if __name__ == "__main__":
    user_question = "give me the graph of total sales by territory"
    user_question = "What is the average value of an order fore each customer segment over the past 100 year?"
    # user_question = "For each product category, how much was sold this year compared to last year? Show the difference and percentage change."
    user_question = "What is the average order value for each customer segment in the last 3 months?"
    user_question = "How many sales representatives are there in each country, and what is the average sales amount?"
    db_path = "dataset/analytics.duckdb"
    sql, result = answer_user_query(db_path, client, user_question)
    print(f"Generated SQL: \n{sql}")
    print("Result:")
    if isinstance(result, str):
        print(result)
    else:
        print(result.to_string(index=False))
    messages = run_analyst_agent(client, result, user_question)
    final_output = normalize_analyst_output(messages["messages"])

    print("Answer:\n", final_output["answer"])
    print("Chart:\n", json.dumps(final_output["chart"], indent=2))

# from app.utils.execute_query import execute_sql_query

# query = """SELECT
# c.customerID,
# c.companyName,
# AVG(od.unitPrice * od.quantity * (1 - od.discount)) AS average_order_value
# FROM
# orders o
# JOIN
# order_details od ON o.orderID = od.orderID
# JOIN
# customers c ON o.customerID = c.customerID
# WHERE
# CAST(o.orderDate) >= DATE '2022-10-01'
# GROUP BY
# c.customerID, c.companyName;
# """
# execute_sql_query(db_path="dataset/analytics.duckdb", query=query)
