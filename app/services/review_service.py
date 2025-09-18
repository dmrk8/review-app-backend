from datetime import datetime
from app.repositories.review_repository import ReviewsCRUD 
from app.models.review_models import ReviewCreate, ReviewDB, ReviewUpdate
from app.models.user_models import UserData

class ReviewService:
    def __init__(self, media_type : str):
        self.repository = ReviewsCRUD(media_type)

    def create_review(self, review_request : ReviewCreate, user_data: UserData):
        review_data = ReviewDB( 
            media_id=review_request.media_id,
            title=review_request.title,
            type=review_request.type,
            rating=review_request.rating,
            review=review_request.review,
            user_id=user_data.id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        try:
            inserted_id = self.repository.create_review(review_data)
            return inserted_id
        
        except Exception as e:
            print("Error creating review in ReviewService:", e)
            raise
    
    def get_reviews_of_user(self, user: UserData):
        return self.repository.get_reviews_by_user_id(user.id)
    
    def update_review(self, update_request : ReviewUpdate, user: UserData):
        user_review_data = self.repository.get_by_id(update_request.review_id)
        
        if not user_review_data:
            raise ValueError(f"Review with id {update_request.id} not found")

        if user_review_data.user_id != user.id:
            raise ValueError(f"not authorized")
         
        user_review_data.updated_at = datetime.now()
        user_review_data.review = update_request.review
        user_review_data.rating = update_request.rating

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
        review_list = self.repository.get_reviews_by_userid(user.id)

        return review_list
        




            

