from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    
class UserData(BaseModel):
    id : Optional[str] = None
    username : str = Field(..., min_length=3, max_length=50)
    hash_password : str = Field(..., min_length=8)
    created_at : datetime = Field(default_factory=datetime.now)  # Auto-generate timestamps
    updated_at : datetime = Field(default_factory=datetime.now)  # Auto-generate timestamps
    role : UserRole = UserRole.USER

class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password : str = Field(..., min_length=8)

