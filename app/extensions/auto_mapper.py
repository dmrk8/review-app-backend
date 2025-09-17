from app.models.anilist_models import Anilist_Media, AniListDTO


def anilist_to_anilistDto(anilistMedia: Anilist_Media) -> AniListDTO:
    try:
        dto = AniListDTO(**anilistMedia.model_dump(include=AniListDTO.model_fields.keys()))
        return dto
    except Exception as e:
        print(f"Error mapping Anilist_Media to DTO: {e}")
        # Either raise a custom exception or return a default
        raise ValueError(f"Failed to map media: {str(e)}")
    
