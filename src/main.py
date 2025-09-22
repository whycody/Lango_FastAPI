from fastapi import FastAPI
from config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from routers import mongo, lemmatize, suggestions

app = FastAPI()
client = AsyncIOMotorClient(settings.mongo_uri)
db = client.get_database()
app.include_router(lemmatize.router)
app.include_router(suggestions.router)
app.include_router(mongo.router)

@app.get("/")
async def root():
    return {"msg": "FastAPI is working.", "port": settings.port}