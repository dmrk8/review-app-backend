
from datetime import datetime
from app.db_layer.review_repository import ReviewsCRUD 
from app.models.review_models import ReviewCreate, ReviewDB, ReviewUpdate
from app.models.user_models import UserData
from app.auth.auth_dependencies import get_current_user
from fastapi import Depends

class ReviewService:
    def __init__(self, media_type : str):
        self.repository = ReviewsCRUD(media_type)

    def create_review(self, review_request : ReviewCreate, user_data: UserData):
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

    def get_all_reviews(self):
        return self.repository.get_all_reviews()

    def get_user_reviews(self, user_data: UserData):
        results = self.repository.get_reviews_by_user_id(user_data.id)

        return results

    def get_review_by_id(self, review_id: str):
        result = self.repository.get_by_id(review_id)

        return result
     
    def delete_review(self, review_id : str, user_id: str):
        try:
            result = self.repository.delete_review(review_id)
            return result 
        
        except Exception as e:
            print("error handling deleting review:", e)
            raise

    def update_review(self, update_request : ReviewUpdate, user_id: str):
        user_review_data = self.repository.get_by_id(update_request.review_id)
        
        if not user_review_data:
            raise ValueError(f"Review with id {update_request.id} not found")

        if user_review_data.user_id != user_id:
            raise ValueError(f"not authorized")
         
        user_review_data.updated_at = datetime.now()
        user_review_data.review = update_request.review
        user_review_data.rating = update_request.rating

        result = self.repository.update_review(user_review_data)
              
        return result

            
    


            

