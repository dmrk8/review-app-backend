from fastapi import FastAPI, Query
import httpx

from app.models.animemodel import Anime

animeApi = FastAPI()

ANILIST_URL = "https://graphql.anilist.co"

@animeApi.get("/anilistSearch")
async def search_anilist(query: str = Query(min_length=1)):
    try:
        anilist_data = await get_from_anilist(query)
        if anilist_data:
            formatted = [format_anilist(media) for media in anilist_data]
            return formatted
    
    except Exception as e:
        print("Anilist failed", e)

    return {"error" : "No data found from any source"}
        
    
async def get_from_anilist(query : str):
    graphql_query = {
        "query": """
        query ($search: String) {
          Page(perPage: 10) {
            media(search: $search, type: ANIME) {
              id
              title {
                romaji
                english
                native
              }
              startDate {
                year
              }
              format
              description 
              coverImage {
                large
                medium
                color 
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


    return data["data"]["Page"]["media"]

def format_anilist(media : dict) -> Anime:
    return Anime(
        title = media["title"].get("english") or media["title"].get("romaji") or "Unknown",
        year = media.get("startDate", {}).get("year"),
        type = media.get("format"),
        description = media.get("description"),
        image = media.get("coverImage", {}).get("large")
    )