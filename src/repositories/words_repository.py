class WordsRepository:
    def __init__(self, db):
        self.collection = db["words"]

    async def get_user_words(self, user_id: str, main_lang: str, translation_lang: str):
        return await self.collection.find(
            {"userId": user_id, "mainLang": main_lang, "translationLang": translation_lang}
        ).to_list(length=None)

    async def update_word(self, word_id: str, update: dict):
        await self.collection.update_one({"_id": word_id}, {"$set": update})