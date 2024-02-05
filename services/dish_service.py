import uuid
from typing import Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Dish
from repositories.dish_repository import DishRepository
from repositories.redis_repository import RedisRepository
from utils import schemas


class DishService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = DishRepository(self.session)
        self.redis = RedisRepository()

    async def create(self, dish: schemas.DishIn, menu_id: uuid.UUID, submenu_id: uuid.UUID) -> Dish:
        created_dish = await self.repository.create(dish, submenu_id)

        await self.redis.delete_parents_and_children_keys(menu_id)

        return created_dish

    async def get(self, submenu_id: uuid.UUID) -> Sequence[Dish]:
        dishes_in_cache = await self.redis.get('dishes_list')

        if dishes_in_cache:
            return dishes_in_cache

        dishes = await self.repository.get(submenu_id)

        await self.redis.save('dishes_list', value=dishes)

        return dishes

    async def get_by_id(self, menu_id: uuid.UUID, submenu_id: uuid.UUID, dish_id: uuid.UUID) -> Dish:
        dish_in_cache = await self.redis.get(menu_id, submenu_id, dish_id)

        if dish_in_cache:
            return dish_in_cache

        dish = await self.repository.get_by_id(dish_id)

        if not dish:
            raise HTTPException(status_code=404, detail='dish not found')

        await self.redis.save(menu_id, submenu_id, dish_id, value=dish)

        return dish

    async def update(self, dish: schemas.DishIn, menu_id: uuid.UUID, dish_id: uuid.UUID) -> Dish:
        updated_dish = await self.repository.update(dish_id, dish)

        await self.redis.delete_parents_and_children_keys(menu_id)

        return updated_dish

    async def delete(self, menu_id: uuid.UUID, dish_id: uuid.UUID) -> schemas.OutAfterDelete:
        await self.repository.delete(dish_id)

        await self.redis.delete_parents_and_children_keys(menu_id)

        return schemas.OutAfterDelete(status=True, message='The dish has been deleted')