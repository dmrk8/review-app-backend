from typing import Optional
from app.models.anilist_models import Anilist_Media, AniListDTO
from app.models.library_models import LibraryReview
from app.models.review_models import ReviewDB


def anilist_to_anilistDto(anilistMedia: Anilist_Media) -> AniListDTO:
    try:
        dto = AniListDTO(**anilistMedia.model_dump(include=set(AniListDTO.model_fields.keys())))
        return dto
    except Exception as e:
        print(f"Error mapping Anilist_Media to DTO: {e}")
        # Either raise a custom exception or return a default
        raise ValueError(f"Failed to map media: {str(e)}")
    
def map_to_library_review(review: ReviewDB, anilist_data: Optional[AniListDTO]) -> LibraryReview:
        if not review.id:
            raise ValueError("Review ID cannot be None.")
        if not review.media_id:
            raise ValueError("Media ID cannot be None.")
        if not review.user_id:
            raise ValueError("User ID cannot be None.") 
        
        
        # Handle None for anilist_data
        if anilist_data is None:
            raise ValueError(f"Data not found for media ID: {review.media_id}")
            
        return LibraryReview(
            review_id=review.id,
            media_id=review.media_id,
            user_id=review.user_id,
            review=review.review,
            rating=review.rating,
            created_at=review.created_at,
            updated_at=review.updated_at,

            # AniList data
            title=anilist_data.title_english,
            description=anilist_data.description,
            start_year=anilist_data.start_year,
            end_year=anilist_data.end_year,
            type=anilist_data.type,
            cover_image=anilist_data.cover_image,
    )
