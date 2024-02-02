import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Dish
from utils import schemas


class DishRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, dish: schemas.DishIn, submenu_id: uuid.UUID) -> Dish:
        dish_obj = Dish(
            id=uuid.uuid4(),
            title=dish.title,
            description=dish.description,
            price=dish.price,
            submenu_id=submenu_id,
        )
        self.session.add(dish_obj)
        await self.session.commit()

        return dish_obj

    async def update(self, dish_id: uuid.UUID, dish: schemas.DishIn) -> Dish:
        dish_obj = await self.get_by_id(dish_id)
        dish_obj.title = dish.title
        dish_obj.description = dish.description
        dish_obj.price = dish.price
        await self.session.commit()

        return dish_obj

    async def delete(self, dish_id: uuid.UUID) -> bool:
        dish = await self.get_by_id(dish_id)
        await self.session.delete(dish)
        await self.session.commit()

        return True

    async def get(self, submenu_id: uuid.UUID) -> Sequence[Dish]:
        res = await self.session.execute(
            select(Dish)
            .where(Dish.submenu_id == submenu_id)
        )
        return res.scalars().all()

    async def get_by_id(self, dish_id: uuid.UUID) -> Dish:
        res = await self.session.execute(
            select(Dish)
            .where(Dish.id == dish_id)
        )
        return res.scalars().one_or_none()
