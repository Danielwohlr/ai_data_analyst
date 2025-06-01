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
    "role": "<chartType>",
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
    
    All available chartTypes (in the "role" key) are listed here: 
    'lineChart' = simple line chart with x and y axis
    'areaChartGradient' = simple line chart with x and y axis with a nice gradient area underneath (use this whenever you can when generating line charts)
    'barChart' = simple bar chart
    'lineChartMultiple' = line chart with x and y axis, with multiple lines in the same plot. You can insert up to 5 y values to create 5 lines. You don't have to always use 5, you can for example use 2 (y1 and y2)
    'tooltip' = a nice way to compare two datasets and show them on a single bar chart type plot
    'barChartHorizontal' = a different orientation of the normal bar chart
    'table' = a standard table, where you can free choose the amount of rows and columns to show data. 
    
    Here is a list of all charts you can create, and their syntax, and example chart outputs:
    (follow the syntax exactly but don't follow the values, they are just placeholders)
    {
        role: 'lineChart', content: {
            chartData: [
                { x: "January", y: 186 },
                { x: "February", y: 305 },
                { x: "March", y: 237 },
                { x: "April", y: 73 },
                { x: "May", y: 209 },
                { x: "June", y: 214 },
            ],
            axisLabels: { x: "Month", y: "Some value" }
        }
    },
    {
        role: 'areaChartGradient', content: {
            chartData: [
                { x: "January", y: 186 },
                { x: "February", y: 305 },
                { x: "March", y: 237 },
                { x: "April", y: 73 },
                { x: "May", y: 209 },
                { x: "June", y: 214 },
            ],
            axisLabels: { x: "Month", y: "Some value" }
        }
    },
    {
        role: 'barChart', content: {
            chartData: [
                { x: "January", y: 186 },
                { x: "February", y: 305 },
                { x: "March", y: 237 },
                { x: "April", y: 73 },
                { x: "May", y: 209 },
                { x: "June", y: 214 },
            ],
            axisLabels: { x: "Month", y: "Some value" }
        }
    },
    {
        role: 'lineChartMultiple',
        content: {
            chartData: [
                { x: "January", y1: 186, y2: 80, y3: 120, y4: 90, y5: 150 },
                { x: "February", y1: 305, y2: 200, y3: 180, y4: 160, y5: 220 },
                { x: "March", y1: 237, y2: 120, y3: 140, y4: 110, y5: 180 },
                { x: "April", y1: 73, y2: 190, y3: 160, y4: 130, y5: 200 },
                { x: "May", y1: 209, y2: 130, y3: 150, y4: 120, y5: 170 },
                { x: "June", y1: 214, y2: 140, y3: 170, y4: 140, y5: 190 }
            ],
            axisLabels: {
                x: "Month",
                y1: "Desktop Users",
                y2: "Mobile Users",
                y3: "Tablet Users",
                y4: "Smart TV Users",
                y5: "Other Devices"
            }
        }
    },
    {
        role: 'tooltip',
        content: {
            chartData: [
                { x: "January", y1: 450, y2: 300 },
                { x: "Feb", y1: 380, y2: 420 },
                { x: "Mar", y1: 520, y2: 120 },
                { x: "Apr", y1: 140, y2: 550 },
                { x: "May", y1: 600, y2: 350 },
                { x: "Jun", y1: 480, y2: 400 }
            ],
            axisLabels: {
                x: "Month",
                y1: "Running",
                y2: "Swimming"
            }
        }
    },
    {
        role: 'barChartHorizontal', content: {
            chartData: [
                { y: "January", x: 186 },
                { y: "February", x: 305 },
                { y: "March", x: 237 },
                { y: "April", x: 73 },
                { y: "May", x: 209 },
                { y: "June", x: 214 },
            ],
            axisLabels: { y: "Month", x: "Some value" }
        }
    },
    {
        role: 'table', content: {
            data: [
                [
                    "INV001", "Paid", "$250.00", "Credit Card",
                ],
                [
                    "INV001", "Paid", "$250.00", "Credit Card",
                ],
                [
                    "INV001", "Paid", "$250.00", "Credit Card",
                ],
                [
                    "INV001", "Paid", "$250.00", "Credit Card",
                ],
                [
                    "INV001", "Paid", "$250.00", "Credit Card",
                ],
                [
                    "INV001", "Paid", "$250.00", "Credit Card",
                ],
                [
                    "INV001", "Paid", "$250.00", "Credit Card",
                ]
            ],
            labels: ["Invoice", "Status", "Method", "Amount"]
        }
    }

    Output rules:
    - Always include the "answer" key.
    - Don't be over confident on what the total database contains because you only see the returned data
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


def format_analyst_result_with_markdown(result, sql_query):
    """
    Formats the 'answer' field of the result (or result itself if it's a string) with markdown.
    Also embeds the SQL query in the markdown.
    """
    markdown_sql = f"```sql\n{sql_query}\n```"

    if isinstance(result, str):
        markdown_answer = (
            f"### Answer\n\n{result}\n\n#### SQL Query Used\n\n{markdown_sql}"
        )
        return markdown_answer

    if isinstance(result, dict):
        answer = result.get("answer", "")
        markdown_answer = (
            f"### Answer\n\n{answer}\n\n#### SQL Query Used\n\n{markdown_sql}"
        )
        result["answer"] = markdown_answer
        return result

    raise ValueError("Unsupported result type. Expected str or dict.")
