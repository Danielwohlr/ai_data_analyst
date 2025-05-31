import json
import pandas as pd


def analyst_agent(
    openai_client, result_df: pd.DataFrame, user_prompt: str
) -> list[dict]:
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
    You are an expert data analyst AI. You will receive a dataset and a user question.

    Your task:
    1. Analyze the dataset and answer the user's question.
    2. Return a single JSON object (not a list).
    3. The JSON object must contain:
    - "answer": a natural language explanation of the answer to the question
    - "chart1": (optional) a chart object if a visual is helpful or requested
    - "chart2": (optional) a second chart object if it improves understanding

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
    - If no charts are needed, return only the "answer" field.
    - Do NOT include markdown, backticks, or text outside the JSON object.
    - Return a valid JSON object.
    """.strip()

    user_content = f"Here is the data:\n{data_str}\n" f"Question: {user_prompt}"
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

    return result


@DeprecationWarning
def normalize_analyst_output(messages):
    """
    Convert the LLM messages to a frontend-ready format with:
    - One text message (string)
    - List of chart objects (if any), normalized to x/y/(series) fields
    """
    if isinstance(messages, dict):
        messages = [messages]

    text_msg = None
    chart_msgs = []

    for msg in messages:
        if msg["role"] == "assistant":
            text_msg = msg["content"]
        elif msg["role"].endswith("Chart"):
            chart_data = msg["content"].get("chartData", [])
            if not chart_data:
                continue

            # Detect keys
            keys = list(chart_data[0].keys())
            x_key = None
            y_key = None
            series_key = None

            for k in keys:
                sample_val = chart_data[0][k]
                if isinstance(sample_val, (int, float)):
                    if not y_key:
                        y_key = k
                else:
                    if not x_key:
                        x_key = k
                    elif not series_key and k != x_key:
                        series_key = k

            # Transform chartData to {x, y, series?}
            transformed_data = []
            for row in chart_data:
                point = {
                    "x": row[x_key],
                    "y": row[y_key],
                }
                if series_key and series_key in row:
                    point["series"] = row[series_key]
                transformed_data.append(point)

            # Default axis labels
            axis_labels = msg["content"].get("axisLabels", {"x": x_key, "y": y_key})
            if series_key:
                axis_labels["series"] = series_key

            chart_msgs.append(
                {
                    "role": msg["role"],
                    "content": {
                        "chartData": transformed_data,
                        "axisLabels": axis_labels,
                    },
                }
            )

    return {
        "answer": text_msg,
        "charts": chart_msgs,
    }
