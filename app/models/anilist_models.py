from pydantic import BaseModel, Field
from typing import List, Optional


class Anilist_Media(BaseModel):
    media_id: int
    title_english: Optional[str] 
    synonyms: List[str] = []
    cover_image: Optional[str] = None
    description: Optional[str] = None
    start_year: Optional[int] 
    end_year: Optional[int] 
    type: str
    
class AniListDTO(BaseModel):
    title_english: str = Field(alias = "title")
    description: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None 
    type: str
    cover_image: Optional[str] = None
    
    class Config:
        populate_by_name = True
    

   
   
