from typing import List, Optional
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from app.models.review_models import ReviewDB
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env

class ReviewsCRUD:
    def __init__(self, media_type : str):
        self.client = MongoClient(os.getenv("MONGODB_URI"), server_api=ServerApi('1'))
        self.db = self.client[os.getenv("DATABASE_NAME")]

        # Pick collection based on media type
        if media_type.upper() == "ANIME":
            self.collection = self.db[os.getenv("ANIME_COLLECTION")]
        elif media_type.upper() == "COMIC" or media_type.upper() == "MANGA":
            self.collection = self.db[os.getenv("MANGA_COLLECTION")]
            
        else:
            raise ValueError("Invalid media_type. Must be 'ANIME' or 'COMIC'.")

    def map_to_model(self, mongo_doc : dict) -> ReviewDB:
        mongo_doc["id"] = str(mongo_doc["_id"])
        mongo_doc.pop("_id", None)
        return ReviewDB(**mongo_doc) #unpack the dictionary into keyword arguments
    
    def create_review(self, review_data : ReviewDB) -> str:
        try:
            data = review_data.model_dump() #map create dictionary from DATA model
            data.pop("id", None)

            result =  self.collection.insert_one(data)
            
            return str(result.inserted_id)
        
        except Exception as e:
            print("error creating review", e)
            raise

    def get_reviews_by_userid(self, user_id : str) -> List[ReviewDB]:
        try:
            cursor = self.collection.find({"user_id": user_id})
            results = [self.map_to_model(doc) for doc in cursor]

            return results
        except Exception as e:
            print(f"Error getting reviews for user {user_id}: {e}")
            raise

    def get_all_reviews(self) -> List[ReviewDB]:
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
            print("error handling deleting review in repo:", e)
            raise


    def update_review(self, updated_data : ReviewDB):
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

    def get_by_id(self, review_id : int) -> Optional[ReviewDB]:
        try:
            data = self.collection.find_one({"_id": ObjectId(review_id)})
            
            if data:
                return self.map_to_model(data)
            
            return None
                
        except Exception as e:
            print(f"Error finding single review by _id {review_id}: {e}")
            raise

    def get_review_by_user_and_media(self, user_id: str, media_id: str):
        try:
            data = self.collection.find_one({"user_id": user_id,
                                            "media_id": media_id})
            if data:
                return self.map_to_model(data)
            return None
        except Exception as e:
            print(f"Error getting review by user id and media id: {e}")
            raise

    def get_reviews(self, user_id: str,
                                      filters: dict,
                                      page: int = 1,
                                      per_page: int = 10,
                                      sort_by: str = "title",
                                      sort_order: int = 1) -> List[ReviewDB]: 
        try:
            query = {"user_id": user_id}
            
            if filters:
                for key, value in filters.items():
                    if key == "title":
                        query[key] = {"$regex": value, "$options": "i"}
                    else:
                        query[key] = value
                query.update(filters) 
            
            skip = (page - 1) * per_page
             
            cursor = self.collection.find(query).sort(sort_by, sort_order).skip(skip).limit(per_page)
            results = [self.map_to_model(doc) for doc in cursor]

            return results
        except Exception as e:
            print(f"Error getting reviews in filtered and sorted for user {user_id}: {e}")
            raise

    
    def count_reviews_by_user(self, user_id: str, filters: dict) -> int:
        try:
            query = {"user_id": user_id}
            if filters:
                query.update(filters) 

            count = self.collection.count_documents(query)
            
            return count
        
        except Exception as e:
            print(f"Error counting reviews  {user_id}: {e}")
            raise








