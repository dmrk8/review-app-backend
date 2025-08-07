from fastapi import FastAPI, Query
import httpx

anilistApi = FastAPI()

ANILIST_URL = "https://graphql.anilist.co"


@anilistApi.get("/anilist/search/anime")
async def search_anime(query: str = Query(min_length=1)):
    anime = await get_anime(query)
    return anime 


@anilistApi.get("/anilist/search/comic")
async def search_comic(query : str = Query(min_length=1)):
    comic = await get_comic(query)
    return comic 
  
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

