import os
from dotenv import load_dotenv
from contextlib import contextmanager
from pymongo import MongoClient
from pymongo.database import Database
from typing import Generator

load_dotenv()

MONGO_DB_HOST = os.getenv("MONGO_DB_HOST")
MONGO_DB_PORT = os.getenv("MONGO_DB_PORT")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_DB_READ_USER = os.getenv("MONGO_DB_READ_USER")
MONGO_DB_READ_USER_PASSWORD = os.getenv("MONGO_DB_READ_USER_PASSWORD")

@contextmanager
def get_mongodb() -> Generator[Database, None, None]:
    """
    Provides a MongoDB database connection using a context manager.
    """
    client = MongoClient(
        host=MONGO_DB_HOST, 
        port=int(MONGO_DB_PORT),
        username=MONGO_DB_READ_USER,
        password=MONGO_DB_READ_USER_PASSWORD,
        authSource=MONGO_DB_NAME
        )
    db = client.get_database(MONGO_DB_NAME)
    try:
        yield db
    finally:
        client.close()
        