from typing import List
from app.services.anilist_service import AnilistService
from app.repositories.review_repository import ReviewsCRUD
from app.models.user_models import UserData
from app.extensions import auto_mapper

class LibraryService:
    def __init__(self):
        self.anilist_service = AnilistService()
        self.anime_repo = ReviewsCRUD("ANIME")
        self.comic_repo = ReviewsCRUD("COMIC")
        
    async def get_user_library(self, user: UserData):
        anime_reviews = self.anime_repo.get_reviews_by_userid(user.id)
        comic_reviews = self.comic_repo.get_reviews_by_userid(user.id)

        all_reviews = anime_reviews + comic_reviews

        media_ids = [r.media_id for r in all_reviews]

        media_list = await self.anilist_service.get_user_media_list(media_ids)

        media_map = {item.media_id: item for item in media_list}
    
        library_reviews = [
            auto_mapper.map_to_library_review(r, media_map.get(r.media_id))
            for r in all_reviews
        ]
        
        return library_reviews
    
    