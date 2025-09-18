
from typing import List
from app.models.anilist_models import Anilist_Media, AniListDTO
from app.integrations.anilistApi import AnilistApi
from app.extensions.auto_mapper import anilist_to_anilistDto

import logging

logger = logging.getLogger(__name__)
class AnilistService:
    def __init__(self):
        self.anilist_api = AnilistApi()

    async def search_anime(self, search : str) -> List[AniListDTO]:
        animes = await self.anilist_api.get_anime(search)

        result_dtos = []

        for anime in animes:
            try:
                AnilistService.set_english_title_if_missing(anime)
                dto = anilist_to_anilistDto(anime)
                result_dtos.append(dto)
            except ValueError as e:
                logger.warning(f"skipping anime due to mapping {e}")
        return result_dtos    

    async def search_comic(self, search : str) -> List[AniListDTO]:
        comics = await self.anilist_api.get_comic(search)
 
        result_dtos = []

        for comic in comics:
            try:
                AnilistService.set_english_title_if_missing(comic)
                dto = anilist_to_anilistDto(comic)
                result_dtos.append(dto)
            except ValueError as e:
                logger.warning(f"skipping comic due to mapping {e}")

        return result_dtos 
    
    async def get_user_media_list(self, id_in: List[int]) -> List[AniListDTO]:
        media_list = await self.anilist_api.get_media_list_by_id_list(id_in)
    
        result_dtos = []

        for media in media_list:
            try:
                AnilistService.set_english_title_if_missing(media)
                dto = anilist_to_anilistDto(media)
                result_dtos.append(dto)
            except ValueError as e:
                logger.warning(f"skipping media due to mapping {e}")

        return result_dtos
    
    @staticmethod 
    def set_english_title_if_missing(media: Anilist_Media) -> None:
        """Set the English title from synonyms if it's missing"""
        if not media.title_english:
            if media.synonyms and len(media.synonyms) > 0:
                media.title_english = media.synonyms[0]
            else:
                media.title_english = f"Unknown {media.type} Title"