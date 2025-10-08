# datamodel.py
from motor.motor_asyncio import AsyncIOMotorClient

class MongoHandler:
    """
    Handles MongoDB connection and insert.
    """
    def __init__(self, uri, db_name, collection_name):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    async def insert_record(self,data):
        """
        Inserts a document into the collection.
        """
        result = await self.collection.insert_one(data)
        return result.inserted_id
