# backend/app/db/connections.py
from sqlalchemy import create_engine
from pymongo import MongoClient
from langchain_community.utilities import SQLDatabase
from ..core.config import settings

# --- MySQL Connection ---
try:
    mysql_engine = create_engine(settings.MYSQL_DATABASE_URL)
    sql_database = SQLDatabase(engine=mysql_engine)
except Exception as e:
    print(f"Error connecting to MySQL: {e}")
    sql_database = None

# --- MongoDB Connection ---
try:
    mongo_client = MongoClient(settings.MONGO_URI)
    mongo_db = mongo_client[settings.MONGO_DB_NAME]
    mongo_collection = mongo_db[settings.MONGO_COLLECTION_NAME]
    # Test connection
    mongo_client.server_info()
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    mongo_collection = None

def get_sql_database():
    """Returns the LangChain SQLDatabase object."""
    return sql_database

def get_mongo_collection():
    """Returns the pymongo collection object."""
    return mongo_collection