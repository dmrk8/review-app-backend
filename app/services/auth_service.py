from fastapi import HTTPException, status
from app.models.user_models import UserLogin
from app.auth.jwt_handler import create_access_token, verify_password
from app.db_layer.user_repository import UserRepository



class AuthService():
    def __init__(self):
        self.user_repository = UserRepository()
         
    def authenticate_user(self, user_login: UserLogin) -> dict:
        try:
            user = self.user_repository.get_by_username(user_login.username)

            if not user or not verify_password(user_login.password, user.hash_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid username or password",
                    headers= {"www-authenticate": "otakutime"}
                )
            
            access_token = create_access_token(
                data={"sub": user.username}
            )

            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "role": user.role
                }
            }
        
        except Exception as e:
            print(f"Error during authentication: {e}")
            raise

