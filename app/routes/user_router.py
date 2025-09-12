from fastapi import APIRouter, Depends, HTTPException
from app.models.user_models import UserLogin
from app.services.user_service import UserService
from app.models.user_models import UserData
from app.auth.auth_dependencies import get_current_user, require_admin

user_router = APIRouter(prefix="/user")
user_service = UserService()

@user_router.post("/register")
async def register(user_data: UserLogin):
    user_id = user_service.create_user(user_data)
    return {"message": "User created successfully", "user_id": user_id}


@user_router.get("/all")
async def get_all_users(current_user: UserData = Depends(require_admin)):
    users =  user_service.get_all_users()

    return [
        {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        } 
        for user in users
    ]

@user_router.get("/getById")
async def get_user_by_id(id : str,
                         current_user: UserData = Depends(require_admin)):
    user = user_service.get_user_by_id(id)
 
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }

