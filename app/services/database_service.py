
from datetime import datetime
from typing import List
from app.db_access.Db_access import ReviewsCRUD 
from app.models.db_models import UserReviewData
from app.models.user_models import UpdateReviewRequest, UserReviewRequest

class ReviewService:
    def __init__(self, media_type : str):
        self.repository = ReviewsCRUD(media_type)

    def create_review(self, review_request : UserReviewRequest):
        review_data = UserReviewData(
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
    
    def delete_review(self, review_id : str):
        try:
            result = self.repository.delete_review(review_id)
            return result 
        
        except Exception as e:
            print("error handling deleting review:", e)
            raise

    def update_review(self, update_request : UpdateReviewRequest):
        user_review_data = self.repository.find_by_id(update_request.id)
        
        if not user_review_data:
            raise ValueError(f"Review with id {update_request.id} not found")
        
        user_review_data.updated_at = datetime.now()
        user_review_data.review = update_request.review
        user_review_data.rating = update_request.rating

        result = self.repository.update_review(user_review_data)
              
        return result

            
    


            

