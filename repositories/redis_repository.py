from typing import Any

import aioredis
import pickle


class RedisRepository:
    def __init__(self):
        self.redis = aioredis.from_url('redis://redis_ylab')

    async def save(self, key: Any, value: Any) -> None:
        key = pickle.dumps(key)
        value = pickle.dumps(value)
        await self.redis.set(key, value, ex=60)

    async def get(self, key: Any) -> Any | None:
        key = pickle.dumps(key)
        value = await self.redis.get(key)

        if not value:
            return None

        value = pickle.loads(value)
        return value

    async def delete(self, key: Any) -> None:
        key = pickle.dumps(key)
        await self.redis.delete(key)

    async def update(self, key: Any, value: Any) -> None:
        await self.delete(key)
        await self.save(key, value)

    async def clear_all(self) -> None:
        await self.redis.flushdb()
