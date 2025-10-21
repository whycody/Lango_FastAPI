from fastapi import APIRouter, Query, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.services.suggestions_service import SuggestionsService
from src.dependencies import get_db

router = APIRouter()

@router.get("/suggestions")
async def get_suggestions(
    user_id: str = Query(...),
    main_lang: str = Query(...),
    translation_lang: str = Query(...),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    service = SuggestionsService(db)
    return await service.get_suggestions(user_id, main_lang, translation_lang)