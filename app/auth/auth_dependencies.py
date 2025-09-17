from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.jwt_handler import verify_token
from app.services.user_service import UserService
from app.models.user_models import UserData, UserRole

security = HTTPBearer()
user_service = UserService()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserData:
    """get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate" : "Bearer"}
    )
    
    token = credentials.credentials #get token from auth header
    username = verify_token(token)

    if username is None:
        raise credentials_exception
    
    user = user_service.get_user_by_username(username)
    if user is None:
        raise credentials_exception
    
    return user

async def require_admin(current_user: UserData = Depends(get_current_user)) -> UserData:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user