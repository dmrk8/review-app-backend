
from datetime import datetime
from typing import Optional
from pydantic import BaseModel



class LibraryReview(BaseModel):
    review_id: str
    media_id : int
    user_id : str

    review: Optional[str] = None
    rating: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    
    title: Optional[str] = None
    description: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    type: str
    cover_image: Optional[str] = None