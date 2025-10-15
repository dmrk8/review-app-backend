from datetime import datetime
from app.repositories.review_repository import ReviewsCRUD 
from app.models.review_models import ReviewCreate, ReviewDB, ReviewUpdate
from app.models.user_models import UserData

class ReviewService:
    def __init__(self, media_type : str):
        self.repository = ReviewsCRUD(media_type)

    def create_review(self, review_request : ReviewCreate, user_data: UserData):
        if not user_data.id:
            raise ValueError("User ID cannot be None.")
    
        existing_review = self.repository.get_review_by_user_and_media(
            user_id=user_data.id, media_id=review_request.media_id
        )

        if existing_review:
            raise ValueError("record already exits")
        if review_request.rating < 0 or review_request.rating > 10:
            raise ValueError("rating must be between 0 and 10")
        
        if len(review_request.review) > 5000:
            raise ValueError("Review must be less than 5000 characters")

            
        review_data = ReviewDB( 
            user_id=user_data.id,
            media_id=review_request.media_id,
            title=review_request.title,
            type=review_request.type,
            rating=review_request.rating,
            review=review_request.review,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        try:
            inserted_id = self.repository.create_review(review_data)
            return inserted_id
        
        except Exception as e:
            print("Error creating review in ReviewService:", e)
            raise
    
    def update_review(self, update_request : ReviewUpdate, user: UserData):
        user_review_data = self.repository.get_by_id(update_request.id)
        
        if not user_review_data:
            raise ValueError(f"Review with id {update_request.id} not found")

        if user_review_data.user_id != user.id:
            raise ValueError(f"not authorized")
        
         
        user_review_data.updated_at = datetime.now()
        user_review_data.review = update_request.review or ""
        user_review_data.rating = update_request.rating or 0.0

        result = self.repository.update_review(user_review_data)
              
        return result
            
    def delete_review(self, review_id : str, user: UserData):
        user_review_data = self.repository.get_by_id(review_id)

        if not user_review_data:
            raise ValueError(f"Review with id {review_id} not found")

        if user_review_data.user_id != user.id:
            raise ValueError(f"not authorized")

        result = self.repository.delete_review(review_id)
        return {"msg:": "review deleted succesfully"} 
        
    def get_reviews_by_userid(self, user: UserData):
        if not user.id:
            raise ValueError("User ID cannot be None.")
        
        review_list = self.repository.get_reviews_by_userid(user.id)

        return review_list
        




            

