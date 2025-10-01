from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

class SuggestionsRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection("suggestions")

    async def get_user_suggestions(self, user_id: str, main_lang: str, translation_lang: str):
        oid = ObjectId(user_id)
        cursor = self.collection.find({
            "userId": oid,
            "mainLang": main_lang,
            "translationLang": translation_lang
        })
        return await cursor.to_list(None)