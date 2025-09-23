from typing import List
import httpx, json

from app.models.anilist_models import Anilist_Media
from app.integrations.redis_client import redis_client
from app.extensions.cache_utils import cache
ANILIST_URL = "https://graphql.anilist.co"
CACHE_DURATION = 60 * 5 
class AnilistApi:
    def __init__(self):
        pass  
    
    @cache(ttl=300)
    async def get_anime(self, query: str) -> List[Anilist_Media]:

        
        graphql_query = {
            "query": """
            query($search: String) {
                Page(perPage: 10) {
                    media(type: ANIME, search: $search) {
                        id
                        title {
                            english
                        }
                        synonyms
                        coverImage {
                            large
                        }
                        description
                        startDate {
                            year
                        }
                        type
                        endDate {
                             year
                        }
                    }
                }
            }
            """,
            "variables": {
                "search": query  
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(ANILIST_URL, json=graphql_query)
            response.raise_for_status()
            data = response.json()

        media_list = map_anilist_to_media(data)

        return media_list

    async def get_comic(self, query: str) -> List[Anilist_Media]:  
        cache_key = f"comic search:{query.lower()}"

        cached = redis_client.get(cache_key)

        if cached:
            data = json.loads(cached)
            return [Anilist_Media(**item) for item in data]
        
        graphql_query = {
            "query": """
            query($search: String) {
                Page(perPage: 10) {
                    media(type: MANGA, search: $search) {
                        id
                        title {
                            english
                        }
                        synonyms
                        coverImage {
                            large
                        }
                        description
                        startDate {
                            year
                        }
                        type
                        endDate {
                             year
                        }
                    }
                }
            }
            """,
            "variables": {
                "search": query  
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(ANILIST_URL, json=graphql_query)
            response.raise_for_status()
            data = response.json()

        media_list = map_anilist_to_media(data)

        await redis_client.setex(
            cache_key,
            CACHE_DURATION,
            media_list
        )
        
        return media_list
    
    async def get_media_list_by_id_list(self, id_in: List[int]) -> List[Anilist_Media]:
        graphql_query = {
            "query": """
            query Page($idIn: [Int]) {
                Page(perPage: 50) {
                    media(id_in: $idIn) {
                        id
                        title {
                            english
                        }
                        synonyms
                        coverImage {
                            large
                        }
                        description
                        startDate {
                            year
                        }
                        type
                        endDate {
                             year
                        }
                    }
                }
            }
            """,
            "variables": {
                "idIn": id_in
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(ANILIST_URL, json=graphql_query)
            response.raise_for_status()
            data = response.json()

        return map_anilist_to_media(data)

def map_anilist_to_media(response: dict) -> List[Anilist_Media]:
    media_list = response.get("data", {}).get("Page", {}).get("media", [])
    
    return [
        Anilist_Media(
            media_id=item.get("id"),
            title_english=item.get("title", {}).get("english"),
            synonyms=item.get("synonyms", []),
            cover_image=item.get("coverImage", {}).get("large"),
            description=item.get("description"),
            start_year=item.get("startDate", {}).get("year"),
            end_year=item.get("endDate", {}).get("year"),
            type=item.get("type"),
        )
        for item in media_list
    ]
