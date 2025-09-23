import redis.asyncio as redis
from Settings import settings
redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True, #work with strings instead of bytes
            username=settings.REDIS_USERNAME,
            password=settings.REDIS_PASSWORD
        )