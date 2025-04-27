import json
import os
from dotenv import load_dotenv
from datetime import datetime
from pymongo import MongoClient, UpdateOne, IndexModel


def read_json():
    try:
        with open('./scripts/mongodb_insert_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        with open('mongodb_insert_data.json', 'r') as file:
            return json.load(file)


if __name__ == '__main__':
    load_dotenv()

    MONGO_DB_HOST = os.getenv("MONGO_DB_HOST", "127.0.0.1")
    try:
        MONGO_DB_PORT = int(os.getenv("MONGO_DB_PORT", 27017))
    except ValueError:
        raise ValueError("MONGO_DB_PORT must be an integer.")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
    MONGO_DB_ADMIN_USER = os.getenv("MONGO_DB_ADMIN_USER")
    MONGO_DB_ADMIN_PASSWORD = os.getenv("MONGO_DB_ADMIN_PASSWORD")
    MONGO_DB_READ_USER = os.getenv("MONGO_DB_READ_USER")
    MONGO_DB_READ_USER_PASSWORD = os.getenv("MONGO_DB_READ_USER_PASSWORD")

    collections = [
        'accessories',
        'insurances',
        'colors',
        'brands',
        'models'
    ]
    
    
    start_time = datetime.now()
    print(f"SEED_MONGODB: {start_time}: Starting MongoDB restore:\n"
          f"MongoDB host: {MONGO_DB_HOST}\n"
          f"MongoDB port: {MONGO_DB_PORT}\n"
          f"MongoDB name: {MONGO_DB_NAME}")

    try:
        data = read_json()

        client = MongoClient(
            host=MONGO_DB_HOST, 
            port=int(MONGO_DB_PORT),
            #username=MONGO_DB_ADMIN_USER,
            #password=MONGO_DB_ADMIN_PASSWORD,
            #authSource='admin'
            )
        
        db = client.get_database(MONGO_DB_NAME)
        
        # Drop and recreate collections with indexes
        db.drop_collection('employees')
        db.create_collection('employees').create_index('email', unique=True)
        
        # Insert data into collections
        for collection_name in collections:
            bulk_operations = [
                UpdateOne({'_id': doc['_id']}, {'$set': doc}, upsert=True)
                for doc in data[collection_name]
            ]
            db.get_collection(collection_name).bulk_write(bulk_operations)

        client.close()
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        print(f"Successfully restored the MongoDB database, it took {duration} seconds.")
    except Exception as error:
        print(f"Error {error.__class__.__name__} caught during Mongo Database restore:\n"
              f"{error}")
