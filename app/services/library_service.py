from typing import List, Optional
from app.services.anilist_service import AnilistService
from app.repositories.review_repository import ReviewsCRUD
from app.models.user_models import UserData
from app.extensions import auto_mapper

class LibraryService:
    def __init__(self, collection_name):
        self.anilist_service = AnilistService()
        self.user_repo = ReviewsCRUD(collection_name)
         
    async def get_user_reviews(self, user: UserData, 
                                page: int,
                                per_page: int,
                                filters: dict,
                                sort_by: str,
                                sort_order: int,
                                ):
        if not user.id:
            raise ValueError("User ID cannot be None.") 
        #get filtered reviews
        user_reviews = self.user_repo.get_reviews(user.id, filters, page, per_page, sort_by, sort_order)

        media_ids = [int(r.media_id) for r in user_reviews]

        media_list = await self.anilist_service.get_user_media_list(media_ids)

        media_map = {item.media_id: item for item in media_list}
    
        library_reviews = [
            auto_mapper.map_to_library_review(r, media_map.get(int(r.media_id)))
            for r in user_reviews
        ]
        
        total = self.user_repo.count_reviews_by_user(user.id, filters)
         
        return {
        "results": library_reviews,
        "page": page,
        "per_page": per_page,
        "total": total,
        "has_next_page": page * per_page < total
    } 
    
    
    
                          