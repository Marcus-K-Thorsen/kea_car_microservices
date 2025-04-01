"""
**MongoDB Connection Module**

This module provides functionality to connect to a MongoDB database using environment variables
for configuration. It includes a context manager to ensure proper handling of the database connection.

Environment Variables:

- `MONGO_DB_HOST`: The hostname of the MongoDB server (default: `127.0.0.1`).
- `MONGO_DB_PORT`: The port number of the MongoDB server (default: `27017`).
- `MONGO_DB_NAME`: The name of the MongoDB database to connect to.
- `MONGO_DB_READ_USER`: The username for read-only access to the database.
- `MONGO_DB_READ_USER_PASSWORD`: The password for the read-only user.

Key Features:

- Securely loads environment variables using `dotenv`.
- Provides a reusable context manager for database connections.
"""

import os
from dotenv import load_dotenv
from contextlib import contextmanager
from pymongo import MongoClient
from pymongo.database import Database
from typing import Generator

# Load environment variables from a .env file
load_dotenv()


# MongoDB configuration
MONGO_DB_HOST = os.getenv("MONGO_DB_HOST", "127.0.0.1")
try:
    MONGO_DB_PORT = int(os.getenv("MONGO_DB_PORT", 27017))
except ValueError:
    raise ValueError("MONGO_DB_PORT must be an integer.")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_DB_READ_USER = os.getenv("MONGO_DB_READ_USER")
MONGO_DB_READ_USER_PASSWORD = os.getenv("MONGO_DB_READ_USER_PASSWORD")


@contextmanager
def get_mongodb() -> Generator[Database, None, None]:
    """
    Provides a MongoDB database connection using a context manager.

    A context manager ensures that the database connection is properly opened and closed,
    even if an exception occurs during its usage. This prevents resource leaks and ensures
    that the connection is always released back to the connection pool.

    Example Usage:
        >>> with get_mongodb() as db:
        >>>     collection = db.get_collection("example_collection")
        >>>     data = collection.find_one({"key": "value"})

    :return: A MongoDB `Database` object for interacting with the specified database.
    :rtype: pymongo.database.Database
    """
    client = MongoClient(
        host=MONGO_DB_HOST, 
        port=MONGO_DB_PORT,
        username=MONGO_DB_READ_USER,
        password=MONGO_DB_READ_USER_PASSWORD,
        authSource=MONGO_DB_NAME,
        connectTimeoutMS=8000,  # 8 seconds timeout for connection establishment
        serverSelectionTimeoutMS=8000  # 8 seconds timeout for server selection
    )
    db = client.get_database(MONGO_DB_NAME)
    try:
        yield db
    finally:
        client.close()
        