import json
import os
import time
from time import sleep
from dotenv import load_dotenv
from datetime import datetime
from pymongo import MongoClient, UpdateOne
from pymongo.database import Database
from typing import Optional


load_dotenv()

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

def read_json():
    try:
        with open('./scripts/mongodb_insert_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        with open('mongodb_insert_data.json', 'r') as file:
            return json.load(file)

def seed_data(db: Database):
    
    
    collections = [
        'employees'
    ]
    
    # Drop and recreate collections with indexes
    db.drop_collection('employees')
    db.create_collection('employees').create_index('email', unique=True)
    
    data = read_json()
    
    # Insert data into collections
    for collection_name in collections:
        bulk_operations = [
            UpdateOne({'_id': doc['_id']}, {'$set': doc}, upsert=True)
            for doc in data[collection_name]
            ]
        db.get_collection(collection_name).bulk_write(bulk_operations)
        
    # Check if the read-only user already exists
    existing_users = db.command("usersInfo", MONGO_DB_APPLICATION_USERNAME)
    if existing_users.get("users"):
        print(f"User '{MONGO_DB_APPLICATION_USERNAME}' already exists in the database '{MONGO_DB_NAME}'.")
    else:
        # Create a read-only user for the database
        db.command("createUser", MONGO_DB_APPLICATION_USERNAME, 
                    pwd=MONGO_DB_APPLICATION_PASSWORD, 
                    roles=[{"role": "read", "db": MONGO_DB_NAME}])
        print(f"Successfully created read-only user '{MONGO_DB_APPLICATION_USERNAME}' for database '{MONGO_DB_NAME}'.")


if __name__ == '__main__':
    # Sleep for 5 seconds
    sleep(5)
    MAX_RETRIES = 10
    RETRY_DELAY = 5  # seconds
    
    start_time = datetime.now()
    print(f"SEED_MONGODB: {start_time}: Starting MongoDB restore:\n"
          f"MongoDB host: {MONGO_DB_HOST}\n"
          f"MongoDB port: {MONGO_DB_PORT}\n"
          f"MongoDB name: {MONGO_DB_NAME}")
    
    client: Optional[MongoClient] = None
    try:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                client = MongoClient(
                    host=MONGO_DB_HOST, 
                    port=MONGO_DB_PORT,
                    username=MONGO_DB_ROOT_USERNAME,
                    password=MONGO_DB_ROOT_PASSWORD,
                    authSource='admin'
                )
                # Try a simple command to check if the connection works
                client.admin.command('ping')
                print(f"Connected to MongoDB on attempt {attempt}.")
                break
            except Exception as error:
                print(f"Attempt {attempt} failed: {error}")
                if attempt == MAX_RETRIES:
                    print("Max retries reached. Exiting.")
                    raise
                time.sleep(RETRY_DELAY)
        
        db = client.get_database(MONGO_DB_NAME)
        
        # Check if the database has already been seeded
        seed_metadata = db.get_collection("seed_metadata")
        if seed_metadata.find_one({"seeded": True}):
            print(f"Database: '{MONGO_DB_NAME}' has already been seeded. Skipping seed script.")
        else:
            seed_data(db)
            # Mark the database as seeded
            seed_metadata.insert_one({"seeded": True, "timestamp": datetime.now()})
            print("Database seeding completed.")
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        print(f"Successfully seeded the MongoDB database: '{MONGO_DB_NAME}', it took {duration} seconds.")
    except Exception as error:
        print(f"Error {error.__class__.__name__} caught during Mongo Database restore:\n"
              f"{error}")
        raise
    finally:
        if client is not None and isinstance(client, MongoClient):
            client.close()
            print("MongoDB connection closed.")
