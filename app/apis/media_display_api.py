from fastapi import APIRouter

from app.anilist.anilistApi import anilistRouter
from app.services.anilist_service import AnilistService

mediaDisplayRouter = APIRouter(prefix="/media")

mediaDisplayRouter.include_router(anilistRouter)

@mediaDisplayRouter.get("/search/anime")
async def search_anime(query: str):
    return await AnilistService.search_anime(query)

@mediaDisplayRouter.get("/search/comic")
async def search_comic(query: str):
    return await AnilistService.search_comic(query)
