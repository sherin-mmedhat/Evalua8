from decouple import config
from pymongo import MongoClient


class MongodbConnection:

    def __init__(self, database):
        self.client = MongoClient(config('MONGO_DB_URI'), int(config('MONGO_DB_PORT')))
        self.db = self.client[database]

    def get_collections(self):
        return self.db.list_collection_names()

    def create_document(self, collection_name, document):
        collection = self.db[collection_name]
        result = collection.insert_one(document)
        return result

    def create_documents(self, collection_name, documents):
        collection = self.db[collection_name]
        result = collection.insert_many(documents)
        return result

    def find_documents(self, collection_name, query=None, projection=None):
        collection = self.db[collection_name]
        result = collection.find(query, projection)
        return list(result)

    def find_document(self, collection_name, query=None, projection=None):
        collection = self.db[collection_name]
        result = collection.find_one(query, projection)
        return result

    def delete_documents(self, collection_name, query=None, projection=None):
        collection = self.db[collection_name]
        result = collection.delete_many(query, projection)
        return result

    def drop_collection(self, collection_name):
        collection = self.db[collection_name]
        result = collection.drop()
        return result
