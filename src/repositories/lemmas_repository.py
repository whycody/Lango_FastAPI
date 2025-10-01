import numpy as np

class LemmasRepository:
    def __init__(self, db):
        self.collection = db["lemmas"]

    async def get_candidates(
            self,
            main_lang: str,
            exclude_lemmas: list,
            recent_lemmas: list = None,
            limit: int = 50
    ):
        query = {"lang": main_lang, "lemma": {"$nin": exclude_lemmas}}

        candidates = await self.collection.find(query).to_list(None)

        median_freq = None
        if recent_lemmas:
            recent_docs_cursor = self.collection.find({"lang": main_lang, "lemma": {"$in": recent_lemmas}})
            recent_docs = await recent_docs_cursor.to_list(None)
            recent_freq_z = [doc.get("freq_z", 0) for doc in recent_docs]
            median_freq = float(np.median(recent_freq_z)) if recent_freq_z else 0.5

            candidates.sort(key=lambda l: abs(l.get("freq_z", 0) - median_freq))

        return {
            "candidates": candidates[:limit],
            "median_freq": median_freq
        }
