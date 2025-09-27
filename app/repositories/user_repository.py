from typing import List
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from app.models.user_models import UserData
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env

class UserRepository:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGODB_URI"), server_api=ServerApi("1"))
        self.db = self.client[os.getenv("DATABASE_NAME")]
        self.collection = self.db[os.getenv("USER_COLLECTION")]

    
    def create(self, user : UserData):
        try:
            data = user.model_dump()
            data.pop("id", None)

            result = self.collection.insert_one(data)
            
            return result

        except Exception as e:
            print(f"Error creating user: {e}")
            raise
    
    def get_by_id(self, id : str) -> UserData:
        try:
            user_doc = self.collection.find_one({"_id": ObjectId(id)})
            
            if user_doc:
                return self.map_to_model(user_doc)

            return None
        
        except Exception as e:
            print(f"Error finding single user by _id {id}: {e}")
            raise
    
    def get_all(self) -> List[UserData]:
        try:
            cursor = self.collection.find()

            results = [self.map_to_model(doc) for doc in cursor] #convert each doc 
                 
            return results
        
        except Exception:
            print("error at getting all users")
            raise            
    
    def update(self, updated_user : UserData):
        try:
            user_dict = updated_user.model_dump()
             
            user_id = user_dict.pop("id", None)
           
            if not user_id:
                raise ValueError("Cannot update user without an id")
             
            result = self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": user_dict}
            )
            return result
        except Exception as e:
            print(f"Error updating user: {e}")
            raise
    
    def delete(self, user_id : str):
        try: 
            result = self.collection.delete_one({"_id" : ObjectId(user_id)})
            return result
        
        except Exception as e:
            print("error handling deleting user:", e)
            raise
    
    def is_username_exists(self, username : str) -> bool:
        try:
            user_doc = self.collection.find_one({"username" : username})
            return user_doc is not None
        
        except Exception as e:
            print(f"Error checking username existence: {e}")
            raise

    def get_by_username(self, username: str) -> UserData:
        try:
            user_doc = self.collection.find_one({"username" : username})

            if user_doc:
                return self.map_to_model(user_doc)
            
            return None

        except Exception as e:
            print(f"Error finding user by username {username}: {e}")
            raise             
    
    def map_to_model(self, mongo_doc : dict) -> UserData:
        mongo_doc["id"] = str(mongo_doc["_id"])
        mongo_doc.pop("_id", None)
        return UserData(**mongo_doc) #unpack the dictionary into keyword arguments


