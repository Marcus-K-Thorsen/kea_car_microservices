import os
from dotenv import load_dotenv
from contextlib import contextmanager
from pymongo import MongoClient
from pymongo.database import Database
from typing import Generator
from src.logger_tool import logger

# Load environment variables from a .env file
load_dotenv()


# MongoDB configuration
MONGO_DB_HOST = os.getenv("MONGO_DB_HOST", "127.0.0.1")
try:
    MONGO_DB_PORT = int(os.getenv("MONGO_DB_PORT", 27017))
except ValueError:
    raise ValueError("MONGO_DB_PORT must be an integer.")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_DB_ROOT_USERNAME = os.getenv("MONGO_DB_ROOT_USERNAME")
MONGO_DB_ROOT_PASSWORD = os.getenv("MONGO_DB_ROOT_PASSWORD")
MONGO_DB_APPLICATION_USERNAME = os.getenv("MONGO_DB_APPLICATION_USERNAME")
MONGO_DB_APPLICATION_PASSWORD = os.getenv("MONGO_DB_APPLICATION_PASSWORD")


@contextmanager
def get_mongodb(as_administrator: bool = False) -> Generator[Database, None, None]:
    logger.info(f"Establishing MongoDB connection with the user: '{MONGO_DB_ROOT_USERNAME if as_administrator else MONGO_DB_APPLICATION_USERNAME}'...")
    client = MongoClient(
        host=MONGO_DB_HOST, 
        port=MONGO_DB_PORT,
        username=MONGO_DB_ROOT_USERNAME if as_administrator else MONGO_DB_APPLICATION_USERNAME,
        password=MONGO_DB_ROOT_PASSWORD if as_administrator else MONGO_DB_APPLICATION_PASSWORD,
        authSource='admin' if as_administrator else MONGO_DB_NAME,
        connectTimeoutMS=8000,  # 8 seconds timeout for connection establishment
        serverSelectionTimeoutMS=8000  # 8 seconds timeout for server selection
    )
    try:
        # Attempt to connect to the database
        db = client.get_database(MONGO_DB_NAME)
        logger.info(f"Successfully connected to MongoDB at {MONGO_DB_HOST}:{MONGO_DB_PORT}")
        yield db
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise
    finally:
        if not as_administrator:
            client.close()
            logger.info("MongoDB connection closed.")
        