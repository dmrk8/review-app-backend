from pydantic import BaseModel
from typing import Optional

class Anime(BaseModel):
    title : str
    year : Optional[int]
    type : Optional[str]
    description : Optional[str]
    image : Optional[str]