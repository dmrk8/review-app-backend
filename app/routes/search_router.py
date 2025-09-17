from fastapi import APIRouter, Query, HTTPException

from app.services.anilist_service import AnilistService

search_router = APIRouter(prefix="/media/search")

anilist_service = AnilistService()

@search_router.get("/anime")
async def search_anime(query: str = Query(min_length=1)):
    try:
        return await anilist_service.search_anime(query)  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching anime: {str(e)}")


@search_router.get("/comic")
async def search_comic(query: str = Query(min_length=1)):
    try:
        return await anilist_service.search_comic(query)  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching comic: {str(e)}")