import openai
import json
import pandas as pd


def run_analyst_agent(
    openai_client, result_df: pd.DataFrame, user_prompt: str
) -> list[dict]:
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
        You are an expert data analyst AI. You will be given a dataset and a user question. 
        Your task is to answer the user's question using the provided data.
        Analyze the data to answer the question. 
        Decide if a chart is appropriate to help explain the answer and if so, or 
        if a chart is useful or requested, include a chart specification as follows: 
        Use this format for your output:
[
  {
    "role": "assistant",
    "content": "<textual explanation of the results in natural language>"
  },
  {
    "role": "<chartType>",
    "content": {
      "chartData": [
        { "x": ..., "y": ..., "series": ... }  // only include 'series' if applicable
      ],
      "axisLabels": { "x": "<Label>", "y": "<Label>" }
    }
  },
  ...
]

Use only JSON. Do NOT include any markdown, backticks, or prose outside the JSON.
Allowed chart types: barChart, lineChart, pieChart, scatterChart.
If the data is not suitable for a chart, just return the textual explanation."
        Provide the final answer in JSON format as a list of messages. The first element should be an assistant message with the explanation of the answer. 
        If a chart is included, the second element should be a chart message with role set to an appropriate chart type (e.g., 'barChart', 'lineChart', etc.), 
        and content containing 'chartData' (the data points) and 'axisLabels' (labels for x and y axes). 
        If no chart is needed, just output a single-element list with the assistant answer. 
        Ensure the JSON is properly formatted.
                """
    user_content = f"Here is the data:\n{data_str}\n" f"Question: {user_prompt}"
    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content},
    ]

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


def normalize_analyst_output(messages):
    """
    Convert the LLM messages to a frontend-ready format with:
    - One text message (string)
    - List of chart objects (if any), normalized to x/y/(series) fields
    """
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
