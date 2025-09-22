from motor.motor_asyncio import AsyncIOMotorDatabase

class SuggestionsRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection("suggestions")

    async def get_user_suggestions(self, user_id: str, main_lang: str, translation_lang: str):
        cursor = self.collection.find({
            "userId": user_id,
            "mainLang": main_lang,
            "translationLang": translation_lang
        })
        return await cursor.to_list(None)