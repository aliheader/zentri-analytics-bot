# SQL Agent with LangChain and GroqCloud

This project implements a SQL Agent using LangChain and LangGraph frameworks, integrated with Vanna for SQL query generation and visualization. The agent uses GroqCloud's Mixtral model for fast inference.

## Features

- Natural language to SQL query conversion using GroqCloud's Mixtral model
- Query rephrasing for better understanding
- Table and column identification
- SQL query validation
- Automatic retry mechanism
- Result visualization
- Error handling and user feedback

## Prerequisites

- Python 3.8+
- GroqCloud API key
- Database connection details

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your configuration:
```env
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=your_database_connection_string
```

## Getting a GroqCloud API Key

1. Sign up for a GroqCloud account at https://console.groq.com/
2. Navigate to the API Keys section
3. Create a new API key
4. Copy the API key and add it to your `.env` file

## Usage

1. Basic usage:
```python
from sql_agent import process_query

result = process_query("Show me the total sales by product category")
print(result["final_message"])
```

2. Run the example script:
```bash
python src/example.py
```

## Workflow

The SQL Agent follows this workflow:
1. Rephrase the natural language query using GroqCloud's Mixtral model
2. Identify relevant tables and columns
3. Generate SQL query using Vanna
4. Validate the generated query
5. If validation fails, retry up to 3 times
6. Generate final message and visualization
7. Return results to the user

## Error Handling

The agent includes:
- Query validation
- Automatic retry mechanism
- Error messages for failed queries
- Visualization of successful queries

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License. 