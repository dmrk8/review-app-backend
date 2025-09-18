from fastapi import APIRouter, HTTPException, Depends

from app.models.review_models import ReviewCreate, ReviewUpdate
from app.models.user_models import UserData
from app.auth.auth_dependencies import get_current_user
from app.services.library_service import LibraryService

library_router = APIRouter(prefix="/library")

@library_router.get("/user-library")
async def get_user_library(
    current_user: UserData = Depends(get_current_user)
):
    try:
        library_service = LibraryService()

        user_library = await library_service.get_user_library(current_user)

        return user_library

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
   