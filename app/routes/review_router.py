from fastapi import APIRouter, HTTPException, Depends

from app.models.review_models import ReviewCreate, ReviewUpdate
from app.models.user_models import UserData
from app.services.library_service import LibraryService
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

@review_router.get("/my-reviews/{media_type}")
async def get_user_reviews(
    media_type: str,
    current_user: UserData = Depends(get_current_user)
):
    
    try:
        review_service = ReviewService(media_type)
        reviews = review_service.get_reviews_of_user(current_user)

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
   
@review_router.put("/update/{media_type}")
async def update_review(
    media_type: str,
    update_request: ReviewUpdate,
    current_user: UserData = Depends(get_current_user)
):
    try:
        review_service = ReviewService(media_type)

        review_service.update_review(update_request, current_user)

        return {"update is a success"} 
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    

@review_router.delete("/delete/{media_type}/{review_id}")
async def delete_review(
    media_type: str,
    review_id: str,
    current_user: UserData = Depends(get_current_user)
):
    try:
        review_service = ReviewService(media_type)

        review_service.delete_review(review_id, current_user)

        return {"message": "delete succesful"}
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))


 
@review_router.get("/library")
async def get_user_library(
    current_user: UserData = Depends(get_current_user)
):
    try:
        library_service = LibraryService()

        user_library = await library_service.get_user_library(current_user)

        return user_library

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 