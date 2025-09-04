from fastapi import APIRouter, HTTPException

from app.models.user_models import UserReviewRequest, UpdateReviewRequest 
from app.services.database_service import ReviewService

userRouter = APIRouter(prefix="/user")

@userRouter.post("/createReview")
async def create_review(review_request: UserReviewRequest):
    try:
        # Initialize service with media type from request
        service = ReviewService(review_request.type)
        inserted_id = service.create_review(review_request)  # Fixed: pass review_request, not UserReviewRequest
        
        return {
            "message": "Review created successfully",
            "review_id": str(inserted_id),
            "title": review_request.title
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating review: {str(e)}")

@userRouter.get("/getAllReviews/{media_type}")
async def get_all_reviews(media_type: str):
    try:
        service = ReviewService(media_type)
        reviews = service.get_all_reviews()
        
        return {
            "reviews": reviews,
            "count": len(reviews)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting reviews: {str(e)}")

@userRouter.delete("/deleteReview/{media_type}") 
async def delete_review(review_id: str, media_type: str):
    try:
        service = ReviewService(media_type)
        result = service.delete_review(review_id)
        
        if result:
            return {"message": "Review deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Review not found")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting review: {str(e)}")

@userRouter.put("/updateReview/{media_type}") 
async def update_review(media_type: str, update_request: UpdateReviewRequest):
    try:
        service = ReviewService(media_type)
        result = service.update_review(update_request)  
        
        if result.modified_count > 0:
            return {"message": "Review updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Review not found")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating review endpoint: {str(e)}")