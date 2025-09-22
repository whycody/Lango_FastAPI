from fastapi import APIRouter
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException
from src.config import settings
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()

client = AsyncIOMotorClient(settings.mongo_uri)
db: AsyncIOMotorDatabase = client.get_database()

@router.get("/health/mongo")
async def check_mongo():
    try:
        count = await db["words"].count_documents({})
        return {"status": "ok", "words_count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mongo connection failed: {e}")