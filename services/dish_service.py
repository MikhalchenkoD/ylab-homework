import uuid
from typing import Sequence

from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Dish
from repositories.discount_repository import DiscountRepository
from repositories.dish_repository import DishRepository
from repositories.redis_repository import RedisRepository
from services.google_sheet_service import GoogleSheetService
from utils import schemas


class DishService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = DishRepository(self.session)
        self.redis = RedisRepository()
        self.google_sheet_service = GoogleSheetService()
        self.discount_repository = DiscountRepository()

    async def create(self, background_tasks: BackgroundTasks, dish: schemas.DishIn, menu_id: uuid.UUID,
                     submenu_id: uuid.UUID) -> Dish:
        created_dish = await self.repository.create(dish, submenu_id)

        background_tasks.add_task(self.redis.delete_parents_and_children_keys, menu_id)

        return created_dish

    async def get(self, submenu_id: uuid.UUID) -> Sequence[Dish]:
        dishes_in_cache = await self.redis.get('dishes_list')

        if dishes_in_cache:
            return dishes_in_cache

        dishes = await self.repository.get(submenu_id)
        updated_dishes_list = []

        for dish in dishes:
            dish_data = await self.google_sheet_service.get_dish_data_by_title(dish.title)

            if dish_data:
                dish = await self.discount_repository.set_discount_for_dish(dish, dish_data['discount'])

            updated_dishes_list.append(dish)

        await self.redis.save('dishes_list', value=updated_dishes_list)

        return updated_dishes_list

    async def get_by_id(self, menu_id: uuid.UUID, submenu_id: uuid.UUID, dish_id: uuid.UUID) -> Dish:
        dish_in_cache = await self.redis.get(menu_id, submenu_id, dish_id)

        if dish_in_cache:
            return dish_in_cache

        dish = await self.repository.get_by_id(dish_id)

        if not dish:
            raise HTTPException(status_code=404, detail='dish not found')

        dish_data = await self.google_sheet_service.get_dish_data_by_title(dish.title)

        if dish_data:
            dish = await self.discount_repository.set_discount_for_dish(dish, dish_data['discount'])

        await self.redis.save(menu_id, submenu_id, dish_id, value=dish)

        return dish

    async def update(self, background_tasks: BackgroundTasks, dish: schemas.DishIn, menu_id: uuid.UUID,
                     dish_id: uuid.UUID) -> Dish:
        updated_dish = await self.repository.update(dish_id, dish)

        if not updated_dish:
            raise HTTPException(status_code=404, detail='dish not found')

        background_tasks.add_task(self.redis.delete_parents_and_children_keys, menu_id)

        dish_data = await self.google_sheet_service.get_dish_data_by_title(updated_dish.title)

        if dish_data:
            updated_dish = await self.discount_repository.set_discount_for_dish(updated_dish, dish_data['discount'])

        return updated_dish

    async def delete(self, background_tasks: BackgroundTasks, menu_id: uuid.UUID,
                     dish_id: uuid.UUID) -> schemas.OutAfterDelete:
        is_deleted = await self.repository.delete(dish_id)

        if not is_deleted:
            raise HTTPException(status_code=404, detail='dish not found')

        background_tasks.add_task(self.redis.delete_parents_and_children_keys, menu_id)

        return schemas.OutAfterDelete(status=True, message='The dish has been deleted')
