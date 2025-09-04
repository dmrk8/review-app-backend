from pydantic import BaseModel, Field
from typing import Optional

class AniListDTO(BaseModel):
    title_english: str = Field(alias = "title")
    description: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None 
    type: str
    cover_image: Optional[str] = None
    
    class Config:
        populate_by_name = True
    

