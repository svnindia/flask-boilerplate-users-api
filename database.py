import pymongo
from bson import ObjectId

__author__ = 'svnindia'


class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient("mongodb://localhost:27017/test_db")
        Database.DATABASE = client.get_default_database()

    @staticmethod
    def insert(collection, data):
        print("WOW ", data)
        return Database.DATABASE[collection].insert_one(data)

    @staticmethod
    def update(collection, _id, data):
        print("update ", data)
        return Database.DATABASE[collection].update({"_id": ObjectId(_id)}, {'$set': data})

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

