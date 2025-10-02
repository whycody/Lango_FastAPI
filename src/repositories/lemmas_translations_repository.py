from typing import List, Dict

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

class LemmasTranslationsRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.lemmas = db["lemmas"]
        self.lemmas_translations = db["lemmas_translations"]

    async def get_untranslated_lemma_ids(
        self,
        main_lang: str,
        translation_lang: str
    ) -> List[str]:
        pipeline = [
            {"$match": {"lang": main_lang}},
            {
                "$lookup": {
                    "from": "lemmas_translations",
                    "localField": "_id",
                    "foreignField": "lemmaId",
                    "as": "translations",
                }
            },
            {"$unwind": "$translations"},
            {
                "$match": {
                    "translations.translationLang": translation_lang,
                    "translations.translation": None,
                }
            },
            {"$project": {"_id": 1}},
        ]

        cursor = self.lemmas.aggregate(pipeline)
        results = await cursor.to_list(length=None)

        return [str(r["_id"]) for r in results]

    async def get_lemmas_translations(
            self,
            lemma_ids: List[str],
            translation_lang: str
    ) -> Dict[str, Dict]:
        cursor = self.lemmas_translations.find({
            "lemmaId": {"$in": [ObjectId(lid) for lid in lemma_ids]},
            "translationLang": translation_lang
        })

        results = await cursor.to_list(length=None)
        return {str(r["lemmaId"]): r for r in results}
