from dotenv import load_dotenv
from openai import OpenAI
import os
import duckdb
import openai
import json

load_dotenv("../.env")  # Load environment variables from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai.api_key)


def answer_query(question: str) -> dict:
    """
    Generate an SQL query from a natural language question using GPT, execute it on a DuckDB database,
    and return the results along with a visualization suggestion.
    Returns a dictionary with keys: 'sql', 'data', 'visualization'.
    """
    # 1. Connect to the DuckDB database (assumes the DuckDB file is available at the given path).
    db_path = "../../../dataset/analytics.duckdb"
    conn = duckdb.connect(database=db_path, read_only=True)
    # 2. Introspect the schema: get tables and columns.
    tables = [table[0] for table in conn.execute("SHOW TABLES").fetchall()]
    schema_lines = []
    for table in tables:
        # Get columns for each table (column name and type)
        cols = conn.execute(f"DESCRIBE {table}").fetchall()
        # Format as "table(col1: type, col2: type, ...)"
        col_defs = ", ".join(
            f"{col_name}: {col_type}" for col_name, col_type, *_ in cols
        )
        schema_lines.append(f"{table}({col_defs})")
    schema_description = "\n".join(schema_lines)

    # 3. Compose the prompt for GPT with a system message to enforce JSON output.
    system_message = (
        "You are an expert data analyst AI. You will be given a database schema and a question. "
        "Write an SQL query to answer the question using the provided schema. "
        "Then suggest an appropriate visualization for the results. "
        "Respond ONLY in JSON format with keys 'sql' and 'visualization'. The 'visualization' value should be an "
        "object specifying a chart type and which fields to use for x-axis, y-axis, and any series grouping."
    )
    user_message = (
        f"### Database Schema:\n{schema_description}\n\n"
        f"### Question:\n{question}\n\n"
        "### Instructions:\nProvide a JSON response with the SQL query and a suggested visualization."
    )
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]

    # 4. Call the OpenAI ChatCompletion API to get the SQL query and visualization suggestion.
    # (Requires openai.api_key to be set in your environment or via openai.api_key attribute)
    response = client.chat.completions.create(
        model="gpt-4o", messages=messages, temperature=0
    )

    assistant_reply = response.choices[0].message.content

    # 5. Parse the assistant's reply as JSON.
    try:
        result_json = json.loads(assistant_reply.strip())
    except json.JSONDecodeError:
        # If the model did not return clean JSON, try to extract JSON substring
        try:
            json_start = assistant_reply.index("{")
            json_end = assistant_reply.rindex("}")
            result_json = json.loads(assistant_reply[json_start : json_end + 1])
        except Exception as e:
            raise RuntimeError(
                f"Failed to parse JSON from GPT response: {e}\nResponse was: {assistant_reply}"
            )

    # Extract the SQL query and visualization info from the parsed JSON.
    sql_query = result_json.get("sql")
    viz_info = result_json.get("visualization")
    if sql_query is None:
        raise RuntimeError(f"No SQL query found in GPT response: {assistant_reply}")

    # 6. Execute the SQL query on DuckDB and fetch results.
    try:
        cur = conn.execute(sql_query)
    except Exception as e:
        # If the query is invalid or fails, you might handle it (e.g., ask GPT to fix it),
        # but for minimal viable version we just raise the error.
        raise RuntimeError(f"SQL query execution failed: {e}")
    # Fetch all rows from the result.
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]  # column names from the result
    # Convert each row tuple to a dict {column: value, ...}
    data = [dict(zip(columns, row)) for row in rows]

    # 7. Prepare the output dictionary.
    output = {"sql": sql_query, "data": data, "visualization": viz_info}
    return output
