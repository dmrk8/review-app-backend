import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId

from app.db_access.db_models import UserReviewData



uri = "mongodb+srv://anildemirok:GAPUh09PTmLDkgTf@anil-mongo-cloud.9p4mqoe.mongodb.net/OtakuTime?retryWrites=true&w=majority&tls=true"


class ReviewsCRUD:
    def __init__(self):
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client["OtakuTime"]
        self.collection = self.db["Reviews"]

    def create_review(self, review_data : UserReviewData) -> str:
        try:
            data = review_data.model_dump()

            data['created_at'] = datetime.datetime.now()
            data['updated_at'] = datetime.datetime.now()

            result =  self.collection.insert_one(data)
            return result.inserted_id
        
        except Exception as e:
            print("error creating review", e)
            raise
            
    def get_all_reviews(self):
        try:
            cursor = self.collection.find()
                 
            results = list(cursor)
            return results
            
        except Exception:
            print("error at getting all reviews")
            raise            
    
    def delete_review(self, review_id : str):
        try: 
            result = self.collection.delete_one({"_id" : ObjectId(review_id)})
            return  result.deleted_count > 0
        
        except Exception as e:
            print("error handling deleting review:", e)
            raise


    def update_review(self, review_id : str, update_data : dict):
        try:
            update_data["updated_at"] = datetime.datetime.now()

            result = self.collection.update_one(
                {"_id" : ObjectId(review_id)},
                {"$set" : update_data}
            )

            return result
        
        except Exception as e:
            print(f"Error updating review: {e}")
            raise
    

    def get_id(self, review_data : UserReviewData) -> str:
        try:
            return str(UserReviewData._id)
        
        except Exception as e:
            print(f"cannot find id: {e}")
            raise






    


