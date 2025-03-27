import json
import os
from dotenv import load_dotenv
from datetime import datetime
from pymongo import MongoClient, UpdateOne, IndexModel


load_dotenv()

MONGO_DB_HOST = os.getenv("MONGO_DB_HOST")
MONGO_DB_PORT = os.getenv("MONGO_DB_PORT")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_DB_ADMIN_USER = os.getenv("MONGO_DB_ADMIN_USER")
MONGO_DB_ADMIN_PASSWORD = os.getenv("MONGO_DB_ADMIN_PASSWORD")

collections = [
    'accessories',
    'insurances',
    'colors',
    'brands',
    'models'
]


def read_json():
    try:
        with open('./scripts/mongodb_insert_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        with open('mongodb_insert_data.json', 'r') as file:
            return json.load(file)


if __name__ == '__main__':
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
            username=MONGO_DB_ADMIN_USER,
            password=MONGO_DB_ADMIN_PASSWORD,
            authSource='admin'
            )
        db = client.get_database(MONGO_DB_NAME)

        db.drop_collection('accessories')
        db.create_collection('accessories').create_index('name', unique=True)
        db.drop_collection('brands')
        db.create_collection('brands').create_index('name', unique=True)
        db.drop_collection('colors')
        db.create_collection('colors').create_index('name', unique=True)
        db.drop_collection('insurances')
        db.create_collection('insurances').create_index('name', unique=True)
        db.drop_collection('models')
        db.create_collection('models').create_indexes([IndexModel('brand._id'), IndexModel('name')])

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
