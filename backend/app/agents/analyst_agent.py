import json
import pandas as pd


def analyst_agent(
    openai_client, result_df: pd.DataFrame, user_prompt: str, sql_query: str
):
    # TODO add table as type of chart (jesse sent example via tg)
    # TODO remove scatterchart, doesnt exist
    # TODO Add Tooltip to chart objects
    """
    Analyze a pandas DataFrame using GPT-4o and a user query,
    and return a structured list of dicts containing the answer and an optional chart specification.
    """
    # 1. Prepare the data string from the DataFrame (use CSV without index for clarity)
    try:
        data_str = result_df.to_csv(index=False)
    except Exception as e:
        # If result_df is not a DataFrame or conversion fails, handle gracefully
        data_str = str(result_df)

    # If the data is very large, consider truncating or summarizing it here.
    # For example, we could limit to first N rows or describe() for large frames.
    if len(data_str) > 10000:  # arbitrary threshold for prompt size
        print("Warning: Data is large, truncating for prompt clarity.")
        data_str = "\n".join(data_str.splitlines()[:50]) + "\n... (data truncated)\n"

    # 2. Construct the prompt messages
    system_content = """
    You are an expert data analyst AI. You will receive a dataset created by a query (also given to you) and a list of the user question with context.
    - THE USER QUESTION IS THE LAST ITEM IN THE question and context LIST. IT IS NOT A JSON OBJECT BUT A STRING. OTHER ITEMS THAT ARE WRAPPED IN JSON OBJECTS ARE PREVIOUS MESSAGES AND ARE JUST CONTEXT.
    - The "content" for role "user" refers to user questions and the "content" for role "assistant" refers to previous assistant answers
    - Use the context for understanding the user question, the question might refer to them.

    Your task:
    1. Analyze the dataset and answer the user's question.
    2. Return a single JSON object (not a list).
    3. The JSON object must contain:
    - "answer": a natural language explanation of the answer to the question
    - "chart1": a chart object if a visual is helpful or requested
    - "chart2": a second chart object if it improves understanding

    Chart format:
    Each chart object must have:
    {
    "role": "<chartType>",  // one of: "barChart", "lineChart", "pieChart", "scatterChart"
    "content": {
        "chartData": [
        { "x": ..., "y": ..., "series": ... }  // include "series" only if needed
        ],
        "axisLabels": {
        "x": "<Label for X axis>",
        "y": "<Label for Y axis>"
        }
    }
    }

    Output rules:
    - Always include the "answer" key.
    - Always use string names for months like "January" not a date like "2015-01"
    - If no charts are needed, return only the "answer" field.
    - Do NOT include markdown, backticks, or text outside the JSON object.
    - Return a valid JSON object.
    """.strip()

    user_content = (
        f"Data received from the database query:\n{data_str}\n"
        f"It was created using this query:\n{sql_query}\n"
        f"List with the Question and context: {user_prompt}"
    )
    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content},
    ]

    print("Analyst agent calling GPT-4o")
    # 3. Call the OpenAI ChatCompletion API with GPT-4o
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0,  # deterministic output for analysis
        response_format={"type": "json_object"},
    )

    # 4. Extract the assistant's message content (which should be a JSON string)
    assistant_reply = response.choices[0].message.content.strip()

    # 5. Parse the JSON string to Python objects
    try:
        result = json.loads(assistant_reply)
    except json.JSONDecodeError as e:
        # If parsing fails (which is unlikely with response_format=json_object),
        # we can attempt to fix minor issues or return an error.
        raise RuntimeError(
            f"Failed to parse LLM response as JSON:\n{assistant_reply}"
        ) from e
    print(f"Analyst agent response: {result}")
    return result
