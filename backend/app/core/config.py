# backend/app/core/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # OpenAI API Key
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # MySQL Database Configuration
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_DB = os.getenv("MYSQL_DB")
    MYSQL_PORT = os.getenv("MYSQL_PORT")
    MYSQL_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB_NAME = "valuefy_clients"
    MONGO_COLLECTION_NAME = "profiles"

settings = Settings()

# Basic validation to ensure keys are loaded
if not settings.OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the .env file")
if not settings.MYSQL_DATABASE_URL:
    raise ValueError("MySQL connection details are not fully set in the .env file")
if not settings.MONGO_URI:
    raise ValueError("MONGO_URI is not set in the .env file")