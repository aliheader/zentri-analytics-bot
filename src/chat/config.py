import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Configuration
host = os.getenv("DB_HOST")
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
port = os.getenv("DB_PORT")
