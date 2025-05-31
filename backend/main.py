from app.core.orchestrator import answer_query
import json

if __name__ == "__main__":
    question = "Show total revenue by country in the last 12 months"
    result = answer_query(question)

    print("\nSQL Query:")
    print(result["sql"])

    print("\nSample Data:")
    for row in result["data"][:5]:  # print first 5 rows
        print(row)

    print("\nSuggested Visualization:")
    print(json.dumps(result["visualization"], indent=2))
