


from typing import List
from app.models.anilist_dto import AniListDTO
from app.models.anilist_models import Anilist_Media
from app.anilist.anilistApi import search_anime, search_comic
from app.extensions.auto_mapper import anilist_to_anilistDto

class AnilistService:
    
    @staticmethod
    async def search_anime(search : str) -> List[AniListDTO]:
        animes = await search_anime(search)

        result_dtos = []

        for anime in animes:
            try:
                AnilistService.set_english_title_if_missing(anime)
                dto = anilist_to_anilistDto(anime)
                result_dtos.append(dto)
            except ValueError as e:
                print(f"Skipping anime due to mapping error: {e}")

        return result_dtos    

    @staticmethod
    async def search_comic(search : str) -> List[AniListDTO]:
        comics = await search_comic(search)

        result_dtos = []

        for comic in comics:
            try:
                AnilistService.set_english_title_if_missing(comic)
                dto = anilist_to_anilistDto(comic)
                result_dtos.append(dto)
            except ValueError as e:
                print(f"Skipping comic due to mapping error: {e}")

        return result_dtos 

    @staticmethod 
    def set_english_title_if_missing(media: Anilist_Media) -> None:
        """Set the English title from synonyms if it's missing"""
        if not media.title_english:
            if media.synonyms and len(media.synonyms) > 0:
                media.title_english = media.synonyms[0]
            else:
                media.title_english = f"Unknown {media.type} Title"