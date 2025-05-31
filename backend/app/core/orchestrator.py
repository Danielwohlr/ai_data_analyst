from dotenv import load_dotenv
from openai import OpenAI
import os
import duckdb
import openai
import json
from app.agents.sql_agent import answer_user_query

load_dotenv(".env")  # Load environment variables from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai.api_key)

answer_user_query()


def answer_query(question: str) -> dict:
    """
    Generate an SQL query from a natural language question using GPT, execute it on a DuckDB database,
    and return the results along with a visualization suggestion.
    Returns a dictionary with keys: 'sql', 'data', 'visualization'.
    """
    # 1. Connect to the DuckDB database (assumes the DuckDB file is available at the given path).
    db_path = "dataset/analytics.duckdb"
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
    system_message = """You are an expert data analyst AI embedded in a chat interface. You will be given:
    1. A database schema
    2. A natural language question

    Your task is to:
    1. Generate an appropriate SQL query using the database schema that is given to you.
    2. Execute the query (assume the result will be available as a list of records)
    3. Write a clear explanation of the result for a non-technical business user
    4. Suggest a visualization based on the query result (only if it makes sense)

    Return your response in JSON format with this structure:

    {
    "sql": "<SQL query string>",
    "message": "<textual explanation of the result, max 3 sentences>",
    "visualization": {
        "type": "<chart type: lineChart | barChart | pieChart | etc>",
        "chartData": [
        { "x": ..., "y": ..., "series": ... }, ...
        ],
        "axisLabels": { "x": "...", "y": "..." }
    }
    }

    - Adhere to DuckDB SQL syntax, e.g. don;t use curdate, use instead current_date.
    - Omit the 'visualization' key if charting is not applicable.
    - Make sure all field names are lowercase and JSON-compliant.
    - If any column like "orderDate" or "shippedDate" is a string, cast it to a DATE or TIMESTAMP before comparing it to date expressions. Example: CAST(orderDate AS DATE)
    - Think well about the databesa schema and the question before generating the SQL query.


    If you understand, wait for the schema and question.
    """
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
        model="gpt-3.5-turbo", messages=messages, temperature=0
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
    # TODO Add check "if visualization"
    return [
        {"role": "user", "content": question},
        {
            "role": "assistant",
            "content": result_json.get("message", "Here is the result."),
        },
        {
            "role": viz_info["type"],
            "content": {
                "chartData": data,
                "axisLabels": viz_info.get("axisLabels", {"x": "x", "y": "y"}),
            },
        },
    ]
