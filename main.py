from fastapi import FastAPI
from config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from routers import lemmatize

app = FastAPI()
client = AsyncIOMotorClient(settings.mongo_uri)
db = client.get_database()
app.include_router(lemmatize.router)

@app.get("/")
async def root():
    return {"msg": "FastAPI is working.", "port": settings.port}