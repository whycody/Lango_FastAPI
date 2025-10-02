from typing import List, Dict

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class LemmasRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.lemmas = db["lemmas"]

    async def fetch_lemmas_by_ids(self, ids: List[str]) -> List[str]:
        object_ids = [ObjectId(i) for i in ids]
        cursor = self.lemmas.find({"_id": {"$in": object_ids}}, {"lemma": 1})
        docs = await cursor.to_list(length=None)
        return [doc["lemma"] for doc in docs if "lemma" in doc]

    async def fetch_lemmas(
            self,
            main_lang: str,
            exclude_lemmas: List[str],
    ) -> List[Dict]:
        query = {"lang": main_lang, "lemma": {"$nin": exclude_lemmas}}
        cursor = self.lemmas.find(query)
        return await cursor.to_list(length=None)

    async def fetch_recent_lemmas(self, main_lang: str, lemmas: List[str]):
        query = {"lang": main_lang, "lemma": {"$in": lemmas}}
        cursor = self.lemmas.find(query)
        return await cursor.to_list(None)
