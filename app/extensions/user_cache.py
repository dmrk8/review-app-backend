import json
import functools
from typing import Callable, Any
from pydantic import BaseModel
from app.integrations.redis_client import redis_client


def user_cache(ttl=900):

    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
           pass 