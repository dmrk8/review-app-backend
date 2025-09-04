






from typing import Optional
from pydantic import BaseModel


class UserReviewRequest(BaseModel):
    """Response model"""
    media_id : int
    title : str
    type : str
    review: str
    rating: float

class UpdateReviewRequest(BaseModel):
    id : str
    review: Optional[str] = None
    rating: Optional[float] = None

 


