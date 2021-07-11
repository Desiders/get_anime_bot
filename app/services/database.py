import asyncio
from typing import List, Optional, Union

import aioredis

from ..utils.scripts import generate_key

USER_KEY = "user_urls"


class RedisDB:
    def __init__(self, host: str, port: int, password: str, db: int):
        self._host = host
        self._port = port
        self._password = password
        self._db = db

        self._redis: Optional[aioredis.RedisConnection] = None
        self._connection_lock = asyncio.Lock()

    async def redis(self) -> aioredis.Redis:
        async with self._connection_lock:
            if self._redis is None or self._redis.closed:
                self._redis = await aioredis.create_redis_pool(address=(self._host, self._port),
                                                               password=self._password,
                                                               db=self._db,
                                                               encoding="utf-8")
        return self._redis

    async def close(self):
        async with self._connection_lock:
            if self._redis and not self._redis.closed:
                self._redis.close()

    async def wait_closed(self):
        async with self._connection_lock:
            if self._redis:
                await self._redis.wait_closed()
    
    async def get_received_urls(self, user_id: Union[str, int]) -> List[str]:
        redis = await self.redis()
        received_urls = await redis.smembers(generate_key(USER_KEY, user_id))
        return received_urls or list()
    
    async def add_received_url(self, user_id: Union[str, int], url: str):
        redis = await self.redis()
        await redis.sadd(generate_key(USER_KEY, user_id), url)
    
    async def clear_received_urls(self, user_id: Union[str, int]):
        redis = await self.redis()
        await redis.unlink(generate_key(USER_KEY, user_id))
