from motor.motor_asyncio import AsyncIOMotorClient
from src.config import settings

client = AsyncIOMotorClient(settings.mongo_uri)
db = client.get_database()

def get_db():
    return db