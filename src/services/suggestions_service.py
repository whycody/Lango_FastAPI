from motor.motor_asyncio import AsyncIOMotorDatabase
from src.repositories.words_repository import WordsRepository
from src.repositories.lemmas_repository import LemmasRepository
from src.repositories.suggestions_repository import SuggestionsRepository
from src.services.lemmatizer import LemmatizerService


class SuggestionsService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.words_repo = WordsRepository(db)
        self.lemmas_repo = LemmasRepository(db)
        self.suggestions_repo = SuggestionsRepository(db)
        self.lemmatizer = LemmatizerService()

    async def _fill_missing_lemmas(self, user_id: str, main_lang: str, translation_lang: str):
        words = await self.words_repo.get_user_words(user_id, main_lang, translation_lang)
        missing_words = [w for w in words if not w.get("lemmas")]

        if missing_words:
            texts = [w["text"] for w in missing_words]

            lemmatized = self.lemmatizer.lemmatize_words(texts, main_lang)

            for word_doc, lemma_result in zip(missing_words, lemmatized):
                word_doc["lemmas"] = lemma_result.lemmas
                await self.words_repo.update_word(
                    word_doc["_id"],
                    {"lemmas": lemma_result.lemmas}
                )

            words = await self.words_repo.get_user_words(user_id, main_lang, translation_lang)

        return words

    async def get_suggestions(self, user_id: str, main_lang: str, translation_lang: str):
        words = await self._fill_missing_lemmas(user_id, main_lang, translation_lang)

        lemma_dates = []
        for w in words:
            for lemma in w.get("lemmas", []):
                lemma_dates.append({"lemma": lemma, "date": w["updatedAt"]})

        suggestion_docs = await self.suggestions_repo.get_user_suggestions(user_id, main_lang, translation_lang)
        for s in suggestion_docs:
            lemma = s.get("lemma")
            if lemma:
                lemma_dates.append({"lemma": lemma, "date": s.get("updatedAt")})

        lemma_dates.sort(key=lambda x: x["date"] or 0, reverse=True)

        recent_lemmas = [ld["lemma"] for ld in lemma_dates[:30]]
        exclude_lemmas = [ld["lemma"] for ld in lemma_dates]

        candidates = await self.lemmas_repo.get_candidates(
            main_lang,
            exclude_lemmas,
            recent_lemmas
        )

        suggested_ids = [str(c["_id"]) for c in candidates]

        return {"suggested_lemmas_ids": suggested_ids}
