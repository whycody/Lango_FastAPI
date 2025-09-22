import numpy as np

class LemmasRepository:
    def __init__(self, db):
        self.collection = db["lemmas"]

    async def get_candidates(self, main_lang: str, exclude_lemmas: list, recent_lemmas: list = None, limit: int = 50):
        query = {"lang": main_lang, "lemma": {"$nin": exclude_lemmas}}

        if not recent_lemmas:
            cursor = self.collection.find(query).sort("freq_z", -1).limit(limit)
            return await cursor.to_list(None)

        recent_freq_z = [lemma["freq_z"] for lemma in recent_lemmas if "freq_z" in lemma]
        if not recent_freq_z:
            median_freq = 0.5
        else:
            median_freq = float(np.median(recent_freq_z))

        candidates = await self.collection.find(query).to_list(None)
        candidates.sort(key=lambda l: abs(l.get("freq_z", 0) - median_freq))

        return candidates[:limit]