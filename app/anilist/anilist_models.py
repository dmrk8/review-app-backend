


from pydantic import BaseModel
from typing import List, Dict, Any


class Media(BaseModel):
    media_id : int
    title : str
    description : str
    startDate : int
    type : str


def map_anilist_response_to_media_list(anilist_data: Dict[str, Any], media_type: str) -> List[Media]:
    media_list = []
    
    for item in anilist_data['data']['Page']['media']:
        # Get English title or fallback to first synonym
        english_title = item.get('title').get('english')
        synonyms = item.get('synonyms')

        title = english_title if english_title else synonyms[0]
    

        media = Media(
            media_id=item.get("id"),
            title= title,
            description=item.get('description'),
            startDate=item.get('startDate').get('year'),
            type=media_type
        )
        media_list.append(media)
    
    return media_list