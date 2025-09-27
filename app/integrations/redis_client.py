import redis.asyncio as redis
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT", 14364)),  # Default port if not set
    decode_responses=True,  # Work with strings instead of bytes
    username=os.getenv("REDIS_USERNAME"),
    password=os.getenv("REDIS_PASSWORD")
)