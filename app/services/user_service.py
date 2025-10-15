from typing import List
from app.repositories.user_repository import UserRepository
from app.models.user_models import UserLogin, UserData
from app.auth.jwt_handler import hash_password


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def create_user(self, user_login : UserLogin) -> str:
        try:
            if self.user_repository.is_username_exists(user_login.username):
                raise ValueError("username is already exists")

            hashed_password = hash_password(user_login.password)

            user_data = UserData(
                username=user_login.username,
                hash_password=hashed_password,
            ) 

            result = self.user_repository.create(user_data)
            return str(result.inserted_id)
        
        except Exception as e:
            print(f"Error creating user: {e}")
            raise