from typing import List
from models import LemmaResult
from nlp_models import models, lemmatize_words_polish


class LemmatizerService:
    @staticmethod
    def lemmatize_words(words: List[str], lang: str) -> List[LemmaResult]:
        if lang not in models and lang != "pl":
            raise ValueError(f"Unsupported language: {lang}")

        results = []
        for w in words:
            if lang == "pl":
                lemmas = lemmatize_words_polish(w)
            else:
                doc = models[lang](w)
                lemmas = [token.lemma_ for token in doc]
            results.append(LemmaResult(word=w, lemmas=lemmas))
        return results