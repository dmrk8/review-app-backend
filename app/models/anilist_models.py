from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class Anilist_Media(BaseModel):
    media_id: int
    title_english: Optional[str] 
    synonyms: List[str] = []
    cover_image: Optional[str] = None
    description: Optional[str] = None
    start_year: Optional[int] 
    end_year: Optional[int] 
    type: str
   
