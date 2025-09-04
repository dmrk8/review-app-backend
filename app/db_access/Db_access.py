import datetime
from typing import List
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId

from app.models.db_models import UserReviewData



uri = "mongodb+srv://anildemirok:GAPUh09PTmLDkgTf@anil-mongo-cloud.9p4mqoe.mongodb.net/OtakuTime?retryWrites=true&w=majority&tls=true"


class ReviewsCRUD:
    def __init__(self, media_type : str):
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client["OtakuTime"]

        # Pick collection based on media type
        if media_type.upper() == "ANIME":
            self.collection = self.db["AnimeReviews"]
        elif media_type.upper() == "COMIC":
            self.collection = self.db["MangaReviews"]
        else:
            raise ValueError("Invalid media_type. Must be 'ANIME' or 'COMIC'.")
        
        
    def create_review(self, review_data : UserReviewData) -> str:
        try:
            data = review_data.model_dump() #map create dictionary from DATA model

            result =  self.collection.insert_one(data)
            return result.inserted_id
        
        except Exception as e:
            print("error creating review", e)
            raise
            
    def get_all_reviews(self) -> List[UserReviewData]:
        try:
            cursor = self.collection.find()

            results = [self.map_to_model(doc) for doc in cursor] #convert each doc 
                 
            return results
            
        except Exception:
            print("error at getting all reviews")
            raise            
    
    def delete_review(self, review_id : str):
        try: 
            result = self.collection.delete_one({"_id" : ObjectId(review_id)})
            return  result
        
        except Exception as e:
            print("error handling deleting review:", e)
            raise


    def update_review(self, updated_data : UserReviewData):
        try:
            data_dict = updated_data.model_dump()
            
            
            review_id = data_dict.pop("id", None)
           
            if not review_id:
                raise ValueError("Cannot update review without an id")
           
            
            result = self.collection.update_one(
                {"_id": ObjectId(review_id)},
                {"$set": data_dict}
            )

            return result

        
        except Exception as e:
            print(f"Error updating review: {e}")
            raise
    
    def find_by_id(self, review_id : int) -> UserReviewData:
        try:
            data = self.collection.find_one({"_id": ObjectId(review_id)})
            
            if data:
                return self.map_to_model(data)
            
            return None
                
        except Exception as e:
            print(f"Error finding single review by _id {review_id}: {e}")
            raise

    def map_to_model(self, mongo_doc : dict) -> UserReviewData:
        mongo_doc["id"] = str(mongo_doc["_id"])
        return UserReviewData(**mongo_doc) #unpack the dictionary into keyword arguments







    


