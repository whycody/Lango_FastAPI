from typing import List

class LemmaResult:
    def __init__(self, word: str, lemmas: List[str]):
        self.word = word
        self.lemmas = lemmas