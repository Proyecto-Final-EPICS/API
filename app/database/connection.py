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
    client = MongoClient(os.getenv('DB_URL', 'http://localhost:27017'))
    return client.cody_db
