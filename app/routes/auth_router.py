from fastapi import APIRouter, Depends
from app.models.user_models import UserLogin
from app.services.auth_service import AuthService
from app.models.user_models import UserData
from app.auth.auth_dependencies import get_current_user, require_admin

auth_router = APIRouter(prefix="/auth", tags=["authentication"])
user_service = AuthService()

@auth_router.post("/login")
async def login(user_data: UserLogin):
    return user_service.authenticate_user(user_data)

@auth_router.get("/me")
async def get_current_user_info(current_user: UserData = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role,
        "created_at": current_user.created_at
    }