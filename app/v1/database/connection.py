from pymongo import MongoClient
from flask import jsonify
import datetime
import os


def get_db():
    # client = MongoClient(host='api_forgames_mongo_1',
    #                      port=27017,
    #                      username='root',
    #                      password='pass',
    #                      authSource="admin")
    # db = client["cody_db"]
    # print(os.getenv('DB_URL1', None))
    # print(os.getenv('DB_NAME1', None))
    client = MongoClient(os.getenv('DB_URL1', 'http://localhost:27017'))
    return client.get_database(os.getenv('DB_NAME1', None))