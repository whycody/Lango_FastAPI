from typing import List, Dict
import numpy as np

from src.repositories.lemmas_repository import LemmasRepository
from src.repositories.lemmas_translations_repository import LemmasTranslationsRepository


class LemmasService:
    def __init__(
            self,
            lemmas_repo: LemmasRepository,
            lemmas_translations_repo: LemmasTranslationsRepository
    ):
        self.lemmas_repo = lemmas_repo
        self.lemmas_translations_repo = lemmas_translations_repo

    async def get_candidates(
            self,
            main_lang: str,
            translation_lang: str,
            exclude_lemmas: List[str],
            recent_lemmas: List[str],
            limit: int = 30
    ) -> Dict:
        lemmas = await self.lemmas_repo.fetch_lemmas(main_lang, exclude_lemmas)

        lemma_ids = [l["_id"] for l in lemmas]
        translation_map = await self.lemmas_translations_repo.get_lemmas_translations(
            [str(lid) for lid in lemma_ids], translation_lang
        )

        median_freq = 0.5
        if recent_lemmas:
            recent_docs = await self.lemmas_repo.fetch_recent_lemmas(main_lang, recent_lemmas)
            recent_freq_z = [doc.get("freq_z", 0) for doc in recent_docs]
            median_freq = float(np.median(recent_freq_z)) if recent_freq_z else 0.5
            lemmas.sort(key=lambda l: abs(l.get("freq_z", 0) - median_freq))

        size = len(lemmas)
        scored_lemmas = []
        for index, l in enumerate(lemmas):
            points = size - index
            lt = translation_map.get(str(l["_id"]))
            add_count = lt.get("addCount", 0) if lt else 0
            skip_count = lt.get("skipCount", 0) if lt else 0
            total_points = points + add_count - skip_count
            scored_lemmas.append({
                "lemma": l,
                "points": total_points
            })

        scored_lemmas.sort(key=lambda x: x["points"], reverse=True)

        candidates = [s["lemma"] for s in scored_lemmas[:limit]]

        return {
            "candidates": candidates,
            "median_freq": median_freq
        }
