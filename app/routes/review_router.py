from fastapi import APIRouter, HTTPException, Depends

from app.models.review_models import ReviewCreate
from app.models.user_models import UserData
from app.services.review_service import ReviewService
from app.auth.auth_dependencies import get_current_user

review_router = APIRouter(prefix="/review")

@review_router.post("/create")
async def create_review(
    review_request: ReviewCreate,
    current_user: UserData = Depends(get_current_user)
):
    
    try:
        review_service = ReviewService(review_request.type)
        result = review_service.create_review(review_request, current_user)
        return {"message": "Review created successfully", "review_id": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    

@review_router.get("/my-reviews")
async def get_all_reviews(
    media_type: str,
    current_user: UserData = Depends(get_current_user)
):
    
    try:
        review_service = ReviewService(media_type)
        reviews = review_service.get_all_reviews()

        return [
            {
                "id": review.id,
                "user_id": review.user_id,
                "media_id": review.media_id,
                "title": review.title,
                "review": review.review,
                "rating": review.rating,
                "type": review.type,
                "created_at": review.created_at,
                "updated_at": review.updated_at
            }
            for review in reviews
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
   

@review_router.delete("/delete") 
async def delete_review(
    review_id: str,
    media_type: str,
    current_user: UserData = Depends(get_current_user)
):
    
        review_service = ReviewService(media_type)
        reviews = review_service.delete_review()
        pass



@review_router.put("update") 
async def update_review(media_type: str, update_request: dict):
    pass