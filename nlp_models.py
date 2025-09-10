from typing import List

import spacy
import morfeusz2

morfeusz = morfeusz2.Morfeusz()

models = {
    "en": spacy.load("en_core_web_sm"),
    "es": spacy.load("es_core_news_sm"),
    "it": spacy.load("it_core_news_sm"),
}

def lemmatize_words_polish(text: str) -> List[str]:
    words = text.split()
    lemmas = [lemmatize_polish(w) for w in words]
    return lemmas

def lemmatize_polish(word: str) -> str:
    analyses = morfeusz.analyse(word)
    if analyses:
        lemma_tag = analyses[0][2][1]
        return lemma_tag.split(":")[0]
    return word