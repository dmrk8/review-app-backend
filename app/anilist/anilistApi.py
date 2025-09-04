from typing import List
from fastapi import APIRouter, Query
import httpx

from app.models.anilist_models import Anilist_Media

anilistRouter = APIRouter(prefix="/anilist/search")

ANILIST_URL = "https://graphql.anilist.co"


@anilistRouter.get("/anime")
async def search_anime(query: str = Query(min_length=1)):
    raw_data = await get_anime(query)
    return map_anilist_to_media(raw_data)


@anilistRouter.get("/comic")
async def search_comic(query : str = Query(min_length=1)):
    raw_data = await get_comic(query)
    return map_anilist_to_media(raw_data)

  
async def get_anime(query: str):
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
            "search" : query  
        }
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(ANILIST_URL, json=graphql_query)
        response.raise_for_status()
        data = response.json()

    return data

 
async def get_comic(query: str):
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
            "search" : query  
        }
    }
    

 
    async with httpx.AsyncClient() as client:
        response = await client.post(ANILIST_URL, json=graphql_query)
        response.raise_for_status()
        data = response.json()

    return data


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
