import pickle
from typing import Any

import aioredis

from converters.redis_converter import RedisConverter


class RedisRepository:
    def __init__(self):
        self.redis = aioredis.from_url('redis://redis_ylab')
        self.converter = RedisConverter()

    async def save(self, *keys: Any, value: Any) -> None:
        key = await self.converter.generate_key(*keys)

        value = pickle.dumps(value)
        await self.redis.set(key, value, ex=60)

    async def get(self, *keys: Any) -> Any | None:
        key = await self.converter.generate_key(*keys)
        value = await self.redis.get(key)

        if not value:
            return None

        value = pickle.loads(value)
        return value

    async def delete_parents_and_children_keys(self, key: Any) -> None:
        keys = await self.get_all_parents_and_children_keys(key)

        for key in keys:
            await self.redis.delete(key)

    async def delete(self, *keys: Any) -> None:
        for key in keys:
            await self.redis.delete(str(key))

    async def get_all_parents_and_children_keys(self, key) -> list[str]:
        keys = ['menus_list', 'submenus_list', 'dishes_list']
        matching_keys = []
        cursor = b'0'

        while cursor:
            cursor, keys_batch = await self.redis.scan(cursor, match=f'{key}*')
            matching_keys.extend(keys_batch)

        return matching_keys + keys
