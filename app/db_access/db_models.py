


import datetime
from typing import Optional
from pydantic import BaseModel


class UserReviewData(BaseModel):
    """Response model"""
    _id : Optional[str] = None
    media_id: int
    title: str
    review: str
    type: str
    rating: float
    created_at : datetime.datetime
    updated_at : datetime.datetime
