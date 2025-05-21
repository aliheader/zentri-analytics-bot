from typing import Dict, List, Optional, TypedDict, Any
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END, START
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
import logging
from datetime import datetime
from pathlib import Path
from src.chat.vanna_model_oai import VannaModelOAI

# from vanna_model import VannaModel
from openai import OpenAI
from src.chat.extract_schema import extract_schema_summary
import json
from plotly.io import write_html
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("sql_agent.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def parse_sql_guidelines() -> str:
    """
    Parse the SQL query guidelines file and create a concise version for prompts.
    Returns a string containing the essential guidelines.
    """
    try:
        guidelines_path = Path("src/chat/training/sql_query_guidelines.md")
        with open(guidelines_path, "r") as f:
            content = f.read()

        # Parse the markdown content into sections
        sections = {}
        current_section = None
        current_content = []

        for line in content.split("\n"):
            line = line.strip()
            if not line:
                continue

            # Check for main sections (##)
            if line.startswith("## "):
                if current_section:
                    sections[current_section] = current_content
                current_section = line[3:].strip()
                current_content = []
            # Check for subsections (###)
            elif line.startswith("### "):
                if current_section:
                    sections[current_section] = current_content
                current_section = line[4:].strip()
                current_content = []
            # Add content to current section
            elif current_section:
                if line.startswith("- "):
                    current_content.append(line[2:])
                else:
                    current_content.append(line)

        # Add the last section
        if current_section:
            sections[current_section] = current_content

        # Extract and format key sections
        guidelines = {
            "core_tables": [],
            "key_relationships": [],
            "query_rules": [],
            "common_pitfalls": [],
        }

        # Map markdown sections to our guidelines structure
        if "1. Schema Overview" in sections:
            if "Core Tables and Relationships" in sections:
                guidelines["core_tables"] = [
                    line
                    for line in sections["Core Tables and Relationships"]
                    if not line.startswith("The database")
                ]
            if "Key Relationships" in sections:
                guidelines["key_relationships"] = sections["Key Relationships"]

        if "2. Query Generation Rules" in sections:
            for subsection in [
                "2.1 Table Joins",
                "2.2 Aggregation Functions",
                "2.3 Date/Time Handling",
                "2.4 Numeric Operations",
                "2.5 Ordering and limit",
            ]:
                if subsection in sections:
                    guidelines["query_rules"].extend(sections[subsection])

        if "7. Common Pitfalls to Avoid" in sections:
            guidelines["common_pitfalls"] = sections["7. Common Pitfalls to Avoid"]

        # Format the guidelines into a concise string with clear instructions
        formatted_guidelines = f"""IMPORTANT SQL QUERY GUIDELINES - FOLLOW THESE RULES STRICTLY:

                                1. DATABASE STRUCTURE:
                                Core Tables and Their Relationships:
                                {chr(10).join(f"   • {table}" for table in guidelines['core_tables'])}

                                Key Table Relationships:
                                {chr(10).join(f"   • {rel}" for rel in guidelines['key_relationships'])}

                                2. QUERY GENERATION RULES:
                                {chr(10).join(f"   • {rule}" for rule in guidelines['query_rules'])}

                                3. CRITICAL REQUIREMENTS:
                                • Always use UTC timezone conversion for any date/time operations
                                • Always apply LIMIT clause (maximum 1000 rows)
                                • Always use explicit JOIN types (INNER, LEFT, etc.)
                                • Always handle NULL values appropriately
                                • Always use proper type casting for numeric operations
                                • Always use DISTINCT when counting unique values
                                • Always order results (default to DESC) unless specified otherwise

                                4. COMMON PITFALLS TO AVOID:
                                {chr(10).join(f"   • {pitfall}" for pitfall in guidelines['common_pitfalls'])}

                                5. QUERY STRUCTURE ORDER:
                                1. SELECT and column definitions
                                2. FROM and JOIN clauses
                                3. WHERE conditions
                                4. GROUP BY clauses
                                5. HAVING conditions
                                6. ORDER BY clauses
                                7. LIMIT clause

                                Remember: These guidelines are mandatory for generating valid and efficient SQL queries."""

        return formatted_guidelines
    except Exception as e:
        logger.error(f"Error parsing SQL guidelines: {str(e)}")
        return ""


# Configuration
class Config:
    GROQ_MODEL = "llama3-70b-8192"
    GROQ_API_URL = "https://api.groq.com/openai/v1"
    MAX_RETRIES = 3
    PLOT_SAVE_DIR = Path("plots")
    PLOT_SAVE_DIR.mkdir(exist_ok=True)
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    SCHEMA_PATH = "src/chat/training/schema.sql"
    SQL_GUIDELINES = parse_sql_guidelines()


# Extract schema summary once at startup
try:
    SCHEMA_SUMMARY = extract_schema_summary(Config.SCHEMA_PATH)
    logger.info("Schema summary extracted successfully")
except Exception as e:
    logger.error(f"Failed to extract schema summary: {str(e)}")
    SCHEMA_SUMMARY = ""


# Initialize VannaModel
try:
    vanna_model = VannaModelOAI()
    logger.info("VannaModel initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize VannaModel: {str(e)}")
    raise

# Initialize OpenAI client for Groq
client = OpenAI(
    base_url=Config.GROQ_API_URL,
    api_key=Config.GROQ_API_KEY,
)


class AgentState(TypedDict):
    messages: List[Dict[str, str]]
    rephrased_query: Optional[str]
    tables_and_columns: Optional[Dict[str, List[str]]]
    sql_query: Optional[str]
    validation_result: Optional[bool]
    retry_count: int
    final_message: Optional[str]
    plot_data: Optional[pd.DataFrame]
    error: Optional[str]
    plot_figure: Optional[Any]
    error_history: List[str]
    is_analytical: Optional[bool]
    question_type_explanation: Optional[str]


def groq_chat_completion(
    messages: List[Dict[str, str]],
    model: str = Config.GROQ_MODEL,
    temperature: float = 0.7,
) -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Groq API call failed: {str(e)}")
        raise


def rephrase_query(state: AgentState) -> AgentState:
    try:
        messages = [
            {
                "role": "system",
                "content": f"""You are a helpful assistant that rephrases natural language queries to be more precise and clear for SQL generation. 
                            Keep the original meaning but make it more structured. Here is the database schema:\n{SCHEMA_SUMMARY}

                            {Config.SQL_GUIDELINES}""",
            },
            {"role": "user", "content": state["messages"][-1]["content"]},
        ]
        state["rephrased_query"] = groq_chat_completion(messages, temperature=0.7)
        logger.info(f"Query rephrased: {state['rephrased_query']}")
        return state
    except Exception as e:
        logger.error(f"Error in rephrase_query: {str(e)}")
        state["error"] = str(e)
        return state


def get_initial_state(query: str) -> Dict:
    return {
        "messages": [{"role": "user", "content": query}],
        "rephrased_query": None,
        "tables_and_columns": None,
        "sql_query": None,
        "validation_result": None,
        "retry_count": 0,
        "final_message": None,
        "plot_data": None,
        "error": None,
        "plot_figure": None,
        "error_history": [],
        "is_analytical": None,
        "question_type_explanation": None,
    }


def identify_tables_and_columns(state: AgentState) -> AgentState:
    try:
        if not state.get("rephrased_query"):
            state["error"] = (
                "No rephrased query available for table/column identification."
            )
            return state
        error_context = ""
        if state.get("error_history"):
            error_context = f"\nPrevious errors: {' | '.join(state['error_history'])}\n"
        messages = [
            {
                "role": "system",
                "content": f"""You are a database expert. Here is the database schema:
                                {SCHEMA_SUMMARY}
                                {error_context}
                                Analyze the query and identify the relevant tables and columns needed.

                                {Config.SQL_GUIDELINES}

                                Return the response as a JSON object with two keys: 'tables' (list of table names) and 'columns' (list of column names, prefixed with table name, e.g. 'table.column').
                                Return ONLY the JSON object, with no additional text or explanation.
                                Example format:
                                {{
                                    "tables": ["table1", "table2"],
                                    "columns": ["table1.column1", "table2.column2"]
                                }}""",
            },
            {"role": "user", "content": state["rephrased_query"]},
        ]
        response = groq_chat_completion(messages, temperature=0.3)
        try:
            # Extract JSON from response by finding first { and last }
            start_idx = response.find("{")
            end_idx = response.rfind("}") + 1
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON object found in response")
            json_str = response[start_idx:end_idx]
            tables_and_columns = json.loads(json_str)
            # Validate structure
            if (
                not isinstance(tables_and_columns, dict)
                or "tables" not in tables_and_columns
                or "columns" not in tables_and_columns
                or not isinstance(tables_and_columns["tables"], list)
                or not isinstance(tables_and_columns["columns"], list)
            ):
                raise ValueError("Invalid JSON structure")
            state["tables_and_columns"] = tables_and_columns
            state["error"] = None  # Clear any previous errors
        except Exception as e:
            logger.error(
                f"Failed to parse LLM response as JSON: {e}. Response: {response}"
            )
            state["tables_and_columns"] = {"tables": [], "columns": []}
            state["error"] = f"Failed to parse LLM response as JSON: {e}"
            return state  # Return early to prevent further processing
        logger.info(f"Tables and columns identified: {state['tables_and_columns']}")
        return state
    except Exception as e:
        logger.error(f"Error in identify_tables_and_columns: {str(e)}")
        state["error"] = str(e)
        return state


def generate_sql_query(state: AgentState) -> AgentState:
    try:
        error_context = ""
        if state.get("error_history"):
            error_context = f"\nPrevious errors: {' | '.join(state['error_history'])}\n"
        if state["tables_and_columns"]:
            tables = state["tables_and_columns"].get("tables", [])
            columns = state["tables_and_columns"].get("columns", [])
            context = ""
            if tables:
                context += f"Relevant tables: {', '.join(tables)}. "
            if columns:
                context += f"Relevant columns: {', '.join(columns)}. "
            prompt = f"""{context}{error_context} Question: {state['rephrased_query']}
                        {Config.SQL_GUIDELINES}"""
            state["sql_query"] = vanna_model.generate_sql(prompt)
            logger.info(f"SQL query generated: {state['sql_query']}")
        else:
            state["error"] = "No tables or columns identified for SQL generation."
            logger.error(state["error"])
            return state
        return state
    except Exception as e:
        logger.error(f"Error in generate_sql_query: {str(e)}")
        state["error"] = str(e)
        return state


def validate_query(state: AgentState) -> AgentState:
    try:
        try:

            if not vanna_model.model.is_sql_valid(state["sql_query"]):
                raise Exception("Invalid SQL query")

            # Try running the SQL with Vanna
            df = vanna_model.run_sql(state["sql_query"])
            state["plot_data"] = df
            state["validation_result"] = True
            state["final_message"] = (
                "Query executed successfully.\n\n"
                f"SQL Query:\n{state['sql_query']}\n\n"
                "Results:\n" + df.to_string()
            )
            logger.info("SQL query validated and executed successfully.")
        except Exception as e:
            state["validation_result"] = False
            state["final_message"] = f"SQL execution error: {str(e)}"
            logger.error(f"SQL execution error: {str(e)}")
        return state
    except Exception as e:
        logger.error(f"Error in validate_query: {str(e)}")
        state["error"] = str(e)
        return state


def generate_final_message(state: AgentState) -> AgentState:
    """
    Final agent: simply returns the final_message already set in the state by previous agents.
    """
    try:
        logger.info(f"Final message: {state.get('final_message')}")
        return state
    except Exception as e:
        logger.error(f"Error in generate_final_message: {str(e)}")
        state["error"] = str(e)
        return state


def retry_node(state: AgentState) -> AgentState:
    """Handle retry logic with proper state management."""
    try:
        # Initialize error history if not present
        if "error_history" not in state:
            state["error_history"] = []

        # Add current error to history if present
        if state.get("error"):
            state["error_history"].append(state["error"])
            state["error"] = None
        elif state.get("final_message") and not state.get("validation_result", True):
            state["error_history"].append(state["final_message"])
            state["final_message"] = None

        # Limit error history to last 3 errors
        state["error_history"] = state["error_history"][-3:]

        # Increment retry count
        state["retry_count"] = state.get("retry_count", 0) + 1

        # Clear previous results to ensure fresh start
        state["tables_and_columns"] = None
        state["sql_query"] = None
        state["validation_result"] = None
        state["plot_data"] = None
        state["plot_figure"] = None

        logger.info(f"Retry attempt {state['retry_count']} of {Config.MAX_RETRIES}")
        return state
    except Exception as e:
        logger.error(f"Error in retry_node: {str(e)}")
        state["error"] = str(e)
        return state


def should_retry(state: AgentState) -> str:
    """Determine if we should retry or end the workflow."""
    if state.get("retry_count", 0) >= Config.MAX_RETRIES:
        return "end"
    if not state.get("validation_result", True):
        return "retry"
    return "end"


# def generate_plot_and_table(state: AgentState) -> AgentState:
#     try:
#         if state.get("plot_data") is not None:
#             try:
#                 # Use Vanna's methods to generate plotly code and figure
#                 plotly_code = vanna_model.model.generate_plotly_code(
#                     state["rephrased_query"], state["sql_query"], state["plot_data"]
#                 )
#                 fig = vanna_model.model.get_plotly_figure(
#                     plotly_code, state["plot_data"]
#                 )
#                 # Save the plotly figure as an HTML file
#                 plot_id = uuid.uuid4().hex
#                 plot_path = Config.PLOT_SAVE_DIR / f"query_results_{plot_id}.html"
#                 write_html(fig, str(plot_path))
#                 state["plot_figure"] = fig  # Store the figure in the state
#                 state["final_message"] = (
#                     f"Query executed successfully. Results have been visualized and saved as '{plot_path}'.\n\nPlotly code used:\n{plotly_code}"
#                 )
#                 logger.info("Plot and data table generated successfully.")
#             except Exception as e:
#                 logger.error(f"Error generating plot: {str(e)}")
#                 state["final_message"] = f"Error generating plot: {str(e)}"
#         else:
#             state["final_message"] = "No data available to plot."
#             logger.warning("No data available to plot.")
#         return state
#     except Exception as e:
#         logger.error(f"Error in generate_plot_and_table: {str(e)}")
#         state["error"] = str(e)
#         return state


def handle_failures(state: AgentState) -> AgentState:
    """
    Agent to handle all fail scenarios and set an appropriate final_message.
    """
    if state.get("error"):
        state["final_message"] = f"An error occurred: {state['error']}"
        logger.error(f"Failure agent: {state['error']}")
    elif not state.get("validation_result", True):
        # If validation_result is False, final_message should already be set by validate_query
        if not state.get("final_message"):
            state["final_message"] = (
                "SQL validation failed. Please check your query and try again."
            )
        logger.warning(f"Failure agent: {state['final_message']}")
    elif state.get("plot_data") is None:
        state["final_message"] = "No data available to plot."
        logger.warning("Failure agent: No data available to plot.")
    elif state.get("plot_figure") is None:
        state["final_message"] = "Plot could not be generated."
        logger.warning("Failure agent: Plot could not be generated.")
    else:
        # Fallback
        state["final_message"] = "An unknown error occurred."
        logger.error("Failure agent: Unknown error.")
    return state


def question_type_detector(state: AgentState) -> AgentState:
    """
    Detects if the question is analytical (requiring SQL) or not.
    Uses schema information to make more accurate decisions.
    """
    try:
        if not state.get("messages"):
            state["error"] = "No question available for type detection."
            return state

        messages = [
            {
                "role": "system",
                "content": f"""You are a question type detector specialized in analyzing questions about e-commerce and marketing data.
                Analyze the given question and determine if it requires SQL analysis or not.
                
                Available database schema information:
                {SCHEMA_SUMMARY}
                
                Return a JSON object with two fields:
                1. is_analytical: boolean (true if question requires SQL analysis)
                2. explanation: string (brief explanation of your decision)
                
                Guidelines for determining if a question is analytical:
                1. Questions that require ANY data retrieval from the database
                2. Questions that mention specific tables, columns, or data fields
                3. Questions that ask to "show", "display", "list", or "get" information
                4. Questions that require joining tables or combining data
                5. Questions about specific records or data points
                6. Questions that require filtering or searching data
                7. Questions that ask for specific information about orders, customers, products, etc.
                
                Examples of analytical questions:
                - "Show basic order information with customer details"
                - "List all products in the electronics category"
                - "Get customer details for order #123"
                - "Show me orders from last month"
                - "Display product inventory levels"
                - "List all active customers"
                - "Show order status for customer John"
                - "Get product details with prices"
                
                Examples of non-analytical questions:
                - "What is the meaning of ROI?"
                - "How do I interpret this chart?"
                - "What are the best practices for data analysis?"
                - "Can you explain what a funnel is?"
                - "What is the difference between CPC and CPM?"
                - "How do I set up a new marketing campaign?"
                - "What is the process for order fulfillment?"
                - "How do I create a new product category?"
                
                Important: 
                1. If the question asks to retrieve, show, or display ANY data from the database, it is analytical
                2. If the question mentions specific tables, columns, or data fields, it is analytical
                3. If the question requires joining tables or combining data, it is analytical
                4. When in doubt, classify as analytical if the question might require ANY data retrieval""",
            },
            {"role": "user", "content": state["messages"][-1]["content"]},
        ]

        response = groq_chat_completion(messages, temperature=0.3)
        try:
            # Extract JSON from response
            start_idx = response.find("{")
            end_idx = response.rfind("}") + 1
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON object found in response")
            json_str = response[start_idx:end_idx]
            result = json.loads(json_str)

            state["is_analytical"] = result.get("is_analytical", False)
            state["question_type_explanation"] = result.get("explanation", "")

            # Log the decision with more context
            logger.info(
                f"Question type detected: {'analytical' if state['is_analytical'] else 'non-analytical'}\n"
                f"Question: {state['messages'][-1]['content']}\n"
                f"Explanation: {state['question_type_explanation']}"
            )
            return state
        except Exception as e:
            logger.error(
                f"Failed to parse question type detection response: {e}\nResponse: {response}"
            )
            state["error"] = f"Failed to parse question type detection response: {e}"
            return state
    except Exception as e:
        logger.error(f"Error in question_type_detector: {str(e)}")
        state["error"] = str(e)
        return state


def direct_answer_agent(state: AgentState) -> AgentState:
    """
    Handles non-analytical questions by providing direct answers.
    Specialized in e-commerce, marketing, and data analysis concepts.
    """
    try:
        if not state.get("messages"):
            state["error"] = "No question available for answering."
            return state

        messages = [
            {
                "role": "system",
                "content": f"""You are an expert assistant specializing in e-commerce, marketing analytics, and data analysis.
                You have deep knowledge of:
                1. E-commerce metrics and KPIs (ROI, ROAS, CAC, LTV, etc.)
                2. Marketing concepts (CPC, CPM, CTR, conversion rates, etc.)
                3. Data analysis methodologies and best practices
                4. Business intelligence and reporting
                5. Database concepts and data modeling
                
                When answering questions:
                1. Be clear, concise, and well-structured
                2. Provide relevant examples from e-commerce and marketing contexts
                3. Include practical applications and use cases
                4. Reference industry best practices when applicable
                5. Explain technical terms in simple language
                6. If a concept has multiple interpretations, explain the different contexts
                
                For technical concepts:
                - Explain the formula or calculation method
                - Provide typical benchmarks or ranges
                - Explain how it's used in decision-making
                - Mention common pitfalls or misconceptions
                
                For process-related questions:
                - Break down steps clearly
                - Include best practices
                - Mention common challenges
                - Provide tips for success
                
                If you're unsure about something:
                1. Be honest about the uncertainty
                2. Explain what you do know
                3. Suggest alternative approaches or resources
                
                IMPORTANT:
                1. DO NOT generate SQL queries
                2. DO NOT reference specific database tables or columns
                3. DO NOT provide code examples
                4. Focus on explaining concepts and providing guidance
                5. Use examples and analogies to illustrate points
                6. Keep explanations practical and actionable
                
                Remember: Your goal is to help users understand concepts and make better data-driven decisions.""",
            },
            {"role": "user", "content": state["messages"][-1]["content"]},
        ]

        answer = groq_chat_completion(messages, temperature=0.7)
        state["final_message"] = f"Answer: {answer}"
        logger.info("Direct answer generated successfully")
        return state
    except Exception as e:
        logger.error(f"Error in direct_answer_agent: {str(e)}")
        state["error"] = str(e)
        return state


def create_workflow() -> StateGraph:
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("detect_question_type", question_type_detector)
    workflow.add_node("direct_answer", direct_answer_agent)
    workflow.add_node("rephrase", rephrase_query)
    workflow.add_node("identify_tables", identify_tables_and_columns)
    workflow.add_node("generate_sql", generate_sql_query)
    workflow.add_node("validate", validate_query)
    workflow.add_node("retry", retry_node)
    workflow.add_node("handle_failures", handle_failures)
    workflow.add_node("final_message_node", generate_final_message)

    # Add entrypoint edge
    workflow.add_edge(START, "detect_question_type")

    # Add conditional edges based on question type
    workflow.add_conditional_edges(
        "detect_question_type",
        lambda state: (
            "rephrase" if state.get("is_analytical", False) else "direct_answer"
        ),
        {
            "rephrase": "rephrase",
            "direct_answer": "direct_answer",
        },
    )

    # Add edges for analytical path
    workflow.add_edge("rephrase", "identify_tables")
    workflow.add_edge("identify_tables", "generate_sql")
    workflow.add_edge("generate_sql", "validate")

    # Add conditional edges with proper stop conditions
    workflow.add_conditional_edges(
        "validate",
        lambda state: (
            "final_message_node"
            if state.get("validation_result") is True
            else (
                "retry"
                if state.get("retry_count", 0) < Config.MAX_RETRIES
                else "handle_failures"
            )
        ),
        {
            "final_message_node": "final_message_node",
            "retry": "retry",
            "handle_failures": "handle_failures",
        },
    )

    # Add retry edge with condition
    workflow.add_conditional_edges(
        "retry",
        lambda state: (
            "identify_tables"
            if state.get("retry_count", 0) < Config.MAX_RETRIES
            else "handle_failures"
        ),
        {
            "identify_tables": "identify_tables",
            "handle_failures": "handle_failures",
        },
    )

    # Add edge for direct answer path
    workflow.add_edge("direct_answer", "final_message_node")

    workflow.add_edge("handle_failures", "final_message_node")
    workflow.add_edge("final_message_node", END)

    # Configure workflow with recursion limit and proper stop conditions
    workflow.config = {
        "recursion_limit": 10,
        "checkpointer": None,
        "interrupt_before": None,
        "interrupt_after": None,
    }

    return workflow.compile()


app = create_workflow()


def process_query(query: str) -> Dict:
    try:
        initial_state = get_initial_state(query)
        logger.info(f"Processing query: {query}")
        result = app.invoke(initial_state)
        if result.get("error"):
            logger.error(f"Error in query processing: {result['error']}")
        return result
    except Exception as e:
        logger.error(f"Error in process_query: {str(e)}")
        raise


if __name__ == "__main__":
    try:
        query = "What is the monthly revenue trend?"
        result = process_query(query)
        print(result["final_message"])
        sql_query = result["sql_query"]
        print("Extracted Query", sql_query)  # This will give you the SQL query string
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise
