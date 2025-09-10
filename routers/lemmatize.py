from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.lemmatizer import LemmatizerService

router = APIRouter()

class WordsRequest(BaseModel):
    words: List[str]
    lang: str = "en"

class LemmasResponse(BaseModel):
    word: str
    lemmas: List[str]

@router.post("/lemmatize_batch", response_model=List[LemmasResponse])
async def lemmatize_batch(req: WordsRequest):
    try:
        results = LemmatizerService.lemmatize_words(req.words, req.lang)
        return [LemmasResponse(word=r.word, lemmas=r.lemmas) for r in results]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))