from flask_pymongo import pymongo
from bson import ObjectId

__author__ = 'svnindia'


class Database(object):
    URI = os.environ['MONGOURL']
    # 'mongodb+srv://username:password@domain.net/flask?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE'
    # URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client.get_database('flask')

    @staticmethod
    def insert(collection, data):
        return Database.DATABASE[collection].insert_one(data)

    @staticmethod
    def update(collection, _id, data):
        return Database.DATABASE[collection].update({"_id": ObjectId(_id)}, {'$set': data})

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)
