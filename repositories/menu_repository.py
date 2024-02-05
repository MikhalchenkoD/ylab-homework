import uuid
from typing import Any, Sequence

from sqlalchemy import Row, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Dish, Menu, Submenu
from utils import schemas


class MenuRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, menu: schemas.MenuIn) -> Row[Any]:
        menu_obj = Menu(id=uuid.uuid4(), title=menu.title, description=menu.description)
        self.session.add(menu_obj)
        await self.session.commit()

        return await self.get_by_id_with_counts(menu_obj.id)

    async def update(self, menu_id: uuid.UUID, menu: schemas.MenuIn) -> Row[Any]:
        menu_obj = await self.get_by_id(menu_id)
        menu_obj.title = menu.title
        menu_obj.description = menu.description
        await self.session.commit()

        return await self.get_by_id_with_counts(menu_obj.id)

    async def delete(self, menu_id: uuid.UUID) -> bool:
        menu = await self.get_by_id(menu_id)
        await self.session.delete(menu)
        await self.session.commit()

        return True

    async def get(self) -> Sequence[Row[Any]]:
        res = await self.session.execute(
            select(
                Menu,
                func.count(func.distinct(Submenu.id)).label('submenus_count'),
                func.count(func.distinct(Dish.id)).label('dishes_count')
            )
            .outerjoin(Submenu, Menu.id == Submenu.menu_id)
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .group_by(Menu.id, Menu.title, Menu.description)
        )

        return res.fetchall()

    async def get_by_id(self, menu_id: uuid.UUID) -> Menu:
        res = await self.session.execute(
            select(Menu)
            .where(Menu.id == menu_id)
        )

        return res.scalars().one_or_none()

    async def get_by_id_with_counts(self, menu_id: uuid.UUID) -> Row[Any]:
        res = await self.session.execute(
            select(
                Menu,
                func.count(func.distinct(Submenu.id)).label('submenus_count'),
                func.count(func.distinct(Dish.id)).label('dishes_count')
            )
            .outerjoin(Submenu, Menu.id == Submenu.menu_id)
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .where(Menu.id == menu_id)
            .group_by(Menu.id, Menu.title, Menu.description)
        )

        return res.fetchone()
