import pickle
from typing import Any

import aioredis

from converters.redis_converter import RedisConverter


class RedisRepository:
    def __init__(self):
        self.redis = aioredis.from_url('redis://redis_ylab')
        self.converter = RedisConverter()

    async def save(self, *keys: Any, value: Any, ex: int = 300) -> None:
        key = await self.converter.generate_key(*keys)

        value = pickle.dumps(value)
        await self.redis.set(key, value, ex=ex)

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

    async def get_all_parents_and_children_keys(self, key: Any) -> list[str]:
        keys = ['menus_list', 'submenus_list', 'dishes_list', 'menus_list_with_submenus_and_dishes',
                'data_from_google_sheet', 'dishes_data_from_google_sheet']
        matching_keys = []
        cursor = b'0'

        while cursor:
            cursor, keys_batch = await self.redis.scan(cursor, match=f'{key}*')
            matching_keys.extend(keys_batch)

        return matching_keys + keys
