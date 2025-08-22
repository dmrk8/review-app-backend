from fastapi import APIRouter, Query
import httpx

from app.anilist.anilist_models import map_anilist_response_to_media_list

anilistRouter = APIRouter(prefix="/anilist/search")

ANILIST_URL = "https://graphql.anilist.co"


@anilistRouter.get("/anime")
async def search_anime(query: str = Query(min_length=1)):
    raw_data = await get_anime(query)
    return map_anilist_response_to_media_list(raw_data, "ANIME")


@anilistRouter.get("/comic")
async def search_comic(query : str = Query(min_length=1)):
    raw_data = await get_comic(query)
    return map_anilist_response_to_media_list(raw_data, "COMIC")

  
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
                            medium
                            color
                            large
                        }
                        description
                        startDate {
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
                            medium
                            color
                            large
                        }
                        description
                        startDate {
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

