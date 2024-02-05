from typing import Any


class RedisConverter:

    async def generate_key(self, *keys: Any) -> str:
        result_key = []

        for key in keys:
            key = str(key)
            result_key.append(key)
        return '_'.join(result_key)
