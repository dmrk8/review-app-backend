import json
import functools
from typing import Callable, Any, Type
from pydantic import BaseModel
from app.integrations.redis_client import redis_client

def anilits_cache(ttl: int=300, model: Type[BaseModel] = None, is_list: bool = False):
    """ 
     Parameters:
    - ttl: time-to-live in seconds
    - model: Pydantic model class to parse cached data
    - is_list: whether the cached data is a list of models
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            cache_key = f"{func.__name__}:{args}:{kwargs}"

            cached = await redis_client.get(cache_key)

            if cached:
                data = json.loads(cached)

                if model:
                    if is_list:
                        return [model(**item) for item in data]
                    return model(**data)

            result = await func(*args, **kwargs)


            try:
                if is_list:
                    data_to_store = json.dumps([r.dict() for r in result])
                elif model:
                    data_to_store = result.json()
                else:
                    data_to_store = json.dumps(result, default=str)
            except Exception:
                data = json.dumps(result, default=str)  # fallback for non-Pydantic

            await redis_client.setex(cache_key, ttl, data_to_store)

            return result
        return wrapper
    return decorator  