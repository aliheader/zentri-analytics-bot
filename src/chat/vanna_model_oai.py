import os
from typing import Optional, Dict, Any, List, Union
import pandas as pd
from vanna.faiss import FAISS
from vanna.ollama import Ollama
from dotenv import load_dotenv
from src.chat.config import host, dbname, user, password, port
from vanna.openai import OpenAI_Chat


# Load environment variables
load_dotenv()


class MyVanna(FAISS, OpenAI_Chat):
    def __init__(self, config=None):
        FAISS.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)


class VannaModelOAI:
    """Custom Vanna model implementation combining FAISS and Ollama"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Vanna model with FAISS and Ollama backends

        Args:
            config: Configuration dictionary for the model
        """
        self.config = config or {
            "model": "gpt-4.1-mini-2025-04-14",
            "api_key": os.getenv("OPENAI_API_KEY"),
            "allow_llm_to_see_data": True,
        }
        self.model: MyVanna = MyVanna(config=self.config)
        self._setup_database_connection()

    def train_qa(self, questions: Union[List[Dict[str, str]], Dict[str, str]]) -> None:
        """
        Train the model with questions and answers

        Args:
            questions: List of dictionaries with 'question' and 'sql_query' keys,
                     or a single dictionary with these keys
        """
        if isinstance(questions, dict):
            questions = [questions]

        for qa in questions:
            self.model.train(question=qa["question"], sql=qa["sql_query"])

    def _initialize_model(self) -> Any:
        """Initialize the combined FAISS and Ollama model"""

    def _setup_database_connection(self):
        """Set up the database connection using environment variables"""
        db_config = {
            "host": os.getenv("DB_HOST"),
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASS"),
            "port": int(os.getenv("DB_PORT", 5432)),
        }

        self.model.connect_to_postgres(
            host=host, dbname=dbname, user=user, password=password, port=port
        )
        print("Vanna connected to database")

    def train_with_schema(self, schema_file_path: str) -> None:
        """
        Train the model with database schema from SQL file

        Args:
            schema_file_path: Path to the SQL file containing schema definitions
        """
        try:
            with open(schema_file_path, "r") as file:
                ddl_statements = file.read().split(";")
                # Clean up statements by removing empty lines and whitespace
                ddl_statements = [
                    stmt.strip()
                    for stmt in ddl_statements
                    if stmt.strip().replace("\n", "")
                ]

                # Train the model with each DDL statement
                for ddl in ddl_statements:
                    if ddl:  # Ensure the statement is not empty
                        self.model.train(ddl=ddl)
                        print(f"Trained with DDL statement: {ddl[:50]}...")

            print("Schema training completed successfully")
        except Exception as e:
            print(f"Error during schema training: {str(e)}")
            raise

    def train_with_schemas(self, schema_dir: str) -> None:
        """
        Train the model with multiple schema files from a directory

        Args:
            schema_dir: Directory containing SQL schema files
        """
        try:
            # Get all SQL files in the directory
            schema_files = [f for f in os.listdir(schema_dir) if f.endswith(".sql")]

            for schema_file in schema_files:
                file_path = os.path.join(schema_dir, schema_file)
                print(f"Training with schema file: {schema_file}")
                self.train_with_schema(file_path)

            print("All schema files processed successfully")
        except Exception as e:
            print(f"Error processing schema directory: {str(e)}")
            raise

    def train_with_documentation(self, documentation_path: str):
        """
        Train the model with SQL query documentation

        Args:
            documentation_path: Path to the documentation file
        """
        with open(documentation_path, "r") as f:
            documentation = f.read()
            self.model.train(documentation=documentation)

    def get_related_documentation(self, question: str) -> list:
        """
        Get related documentation for a given question

        Args:
            question: The question to find related documentation for

        Returns:
            List of related documentation
        """
        return self.model.get_related_documentation(question)

    def run_sql(self, query: str) -> pd.DataFrame:
        """
        Execute a SQL query and return the results

        Args:
            query: SQL query to execute

        Returns:
            DataFrame containing the query results
        """
        return self.model.run_sql(query)

    def generate_sql(self, question: str) -> str:
        """
        Generate SQL from a natural language question

        Args:
            question: Natural language question

        Returns:
            Generated SQL query
        """
        return self.model.generate_sql(question)

    def ask(self, question: str) -> str:
        """
        Ask a question and get a SQL query response

        Args:
            question: Natural language question

        Returns:
            Generated SQL query
        """
        return self.model.ask(question)

    def get_training_data(self) -> pd.DataFrame:
        """
        Get the current training data

        Returns:
            DataFrame containing the training data
        """
        return self.model.get_training_data()

    def add_training_data(self, question: str, sql: str):
        """
        Add new training data

        Args:
            question: Natural language question
            sql: Corresponding SQL query
        """
        self.model.train(question=question, sql=sql)

    def remove_training_data(self):
        for data in self.get_training_data().to_dict(orient="records"):
            self.model.remove_training_data(data["id"])


def get_vanna_model():
    return VannaModelOAI().model


# Example usage
if __name__ == "__main__":
    # Initialize the model
    vanna_model = VannaModelOAI()

    # # Train with schema
    # vanna_model.train_with_schema("training/schema.sql")

    vanna_model.remove_training_data()
    vanna_model.train_with_schema("training/schema.sql")
    # vanna_model.train_with_schema("training/schema.sql")

    # # Train with example queries
    from training.queries import questions

    vanna_model.train_qa(questions)

    # Example queries
    # example_queries = [
    #     "What is the revenue by product collection?",
    #     "Who are the top 10 customers by total spend?",
    #     "What is the customer acquisition trend by month?",
    # ]

    # # Process each query
    # for query in example_queries:
    #     print(f"\nProcessing query: {query}")
    #     sql = vanna_model.generate_sql(query)
    #     print(f"Generated SQL: {sql}")

    #     try:
    #         result = vanna_model.run_sql(sql)
    #         print("Query Results:")
    #         print(result.head())
    #     except Exception as e:
    #         print(f"Error executing query: {str(e)}")

    # training_data = vanna_model.model.get_training_data()
    # print(training_data.filter(training_data["training_data_type"] == "ddl"))

    # print(vanna_model.get_training_data())

    training_data = vanna_model.model.get_training_data()
    ddl = training_data[(training_data["training_data_type"] == "ddl")]["ddl"]
    for d in ddl:
        print(d)
