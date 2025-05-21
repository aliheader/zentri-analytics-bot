from chat.sql_agent import process_query
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def main():
    # Example queries
    queries = [
        "Show me the total sales by product category for the last quarter",
        "What are the top 5 customers by total purchase amount?",
        "Compare monthly revenue between this year and last year",
    ]

    for query in queries:
        print(f"\nProcessing query: {query}")
        result = process_query(query)
        print(f"Result: {result['final_message']}")

        if result.get("plot_data") is not None:
            print("\nData Preview:")
            print(result["plot_data"].head())


if __name__ == "__main__":
    main()
