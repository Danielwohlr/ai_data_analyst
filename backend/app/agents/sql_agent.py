from app.schemas.build_schema import build_duckdb_schema
from app.utils.execute_query import execute_sql_query
import pandas as pd


def build_user_prompt(user_question, error_messages=None):
    """
    Given a user question, build the user prompt for the chatgpt API
    :param user_question: the user question
    :return: the user prompt
    """
    user_prompt = f"{user_question}"
    user_prompt = (
        user_prompt + f"""Instructions:
        You are a system generating sql code from natural language inputs. The sql you create will be used to fetch data from a duckdb database. 
        - THE CURRENT USER QUESTION IS THE LAST MESSAGE IN THE MESSAGE ARRAY. USE THIS AS THE USER QUESTION. PREVIOUS MESSAGES ARE CONTEXT FOR YOU. 
        - Current timestamp: {pd.Timestamp.now().strftime("%Y-%m-%d")} (format is year-month-day).
        - Use the date info to calculate timeframes. For example last quarter refers to 4 quarters of a year, and last quarter means the previous one that is not ongoing.
        - Also last year refers to the year before the on you see in the timestamp
        """
    )
    if error_messages:
        error_log = "\n".join(f"- {msg}" for msg in error_messages)
        user_prompt += f"""\n\nNOTE: Previous SQL queries failed with these errors:\n{error_log}\nFix them in the next query.\n
        """.strip()
    return user_prompt

def build_system_prompt(schema_description):
    """
    Build the system prompt including schema and past errors.
    """
    instructions_prompt = """
    Given the following SQL tables, your job is to write DuckDB queries to answer the user's questions.
    Respond only with SQL and no additional content. Make sure you use only DuckDB syntax and NOT SQLite or MySQL.
    Do NOT wrap your answer in markdown or backticks.
    If the error is because of comparison of VARCHAR and DATE, CAST explicitly the variable as DATE.
    """.strip()

    return f"{instructions_prompt}\n\n{schema_description}"


def call_chatgpt(openai_client, system_prompt, user_prompt):
    """
    Call the chatgpt API to generate a SQL query
    :param openai_client: The openai clients
    :param system_prompt: The system prompt
    :param user_prompt: The user prompt
    :return: The response from the chatgpt API
    """
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )
    return response


def sql_agent(db_path, openai_client, user_query, max_retries=1):
    """
    Generate SQL using ChatGPT, execute it on DuckDB, retrying on error up to `max_retries`.
    Includes all previous error messages in system prompt.
    """
    schema = build_duckdb_schema(db_path)
    error_messages = []

    for attempt in range(max_retries):
        system_prompt = build_system_prompt(schema)
        user_prompt = build_user_prompt(user_query, error_messages)
        print(f"SQL agent calling ChatGPT")
        chat_response = call_chatgpt(openai_client, system_prompt, user_prompt)
        sql = extract_sql(chat_response)

        try:
            df = execute_sql_query(db_path, sql)
            return sql, df
        except Exception as e:
            error_messages.append(str(e))
            print(f"[Attempt {attempt+1}] SQL execution failed: {e}")

    return (
        sql,
        "The assistant could not generate a valid SQL query after several attempts.",
    )


import re


def extract_sql(response):
    """
    Extract clean SQL from the response content.
    Strips markdown, code fences, and ensures it's valid SQL string.
    """
    content = response.choices[0].message.content.strip()

    # Remove markdown code fences
    if content.startswith("```"):
        content = re.sub(r"^```(?:sql)?", "", content, flags=re.IGNORECASE).strip()
        content = re.sub(r"```$", "", content).strip()

    # Strip leading/trailing whitespace
    content = content.strip()

    # Optional: ensure it starts with SELECT or WITH or some valid SQL starting keyword
    if not re.match(r"^(SELECT|WITH|INSERT|UPDATE|DELETE)", content, re.IGNORECASE):
        raise ValueError(
            f"Extracted content does not appear to be valid SQL:\n{content}"
        )

    return content
