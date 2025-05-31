from app.schemas.build_schema import build_duckdb_schema
from app.utils.execute_query import execute_sql_query


def build_system_prompt(schema_description):
    """
    Given a schema description, build the system prompt for the chatgpt API
    :param schema_description: the database schema as a string
    :return: the system prompt
    """
    instructions_prompt = """
    Given the following SQL tables, your job is to write DuckDB queries to answer the user's questions.
    Respond only with SQL and no additional content.
    """.strip()
    return f"{instructions_prompt}\n{schema_description}"


def build_user_prompt(user_question):
    """
    Given a user question, build the user prompt for the chatgpt API
    :param user_question: the user question
    :return: the user prompt
    """
    return f"{user_question}\nSELECT"


def call_chatgpt(openai_client, system_prompt, user_prompt):
    """
    Call the chatgpt API to generate a SQL query
    :param openai_client: The openai clients
    :param system_prompt: The system prompt
    :param user_prompt: The user prompt
    :return: The response from the chatgpt API
    """
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )
    return response


def answer_user_query(db_path, openai_client, user_query):
    """
    Answer a user query by generating SQL with chatgpt, executing the SQL,
    and returning the results as a DataFrame
    :param engine: the sqlalchemy engine
    :param openai_client: the openai client
    :param user_query: the user query
    :return: A pair containing the sql generated and the results as a DataFrame
    """
    schema = build_duckdb_schema(db_path)
    system_prompt = build_system_prompt(schema)
    user_prompt = build_user_prompt(user_query)
    chat_response = call_chatgpt(openai_client, system_prompt, user_prompt)
    sql = extract_sql(chat_response)
    try:
        df = execute_sql_query(db_path, sql)
    except Exception as e:
        print(f"Error executing SQL: {e}")
        return (
            sql,
            "The assistant could not answer your question. Please try reformulating it.",
        )
    return sql, df


def extract_sql(response):
    """
    extract and format the SQL portion of the response
    :param response: the raw response from the chatgpt API
    :return: the SQL query
    """
    raw_query = response.choices[0].message.content.strip()
    if not raw_query.upper().startswith("SELECT"):
        raw_query = f"SELECT {raw_query}"
    return raw_query
