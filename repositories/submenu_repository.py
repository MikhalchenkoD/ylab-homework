import uuid
from typing import Any, Sequence

from sqlalchemy import Row, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import UnmappedInstanceError

from database.models import Dish, Submenu
from utils import schemas


class SubmenuRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, submenu: schemas.SubmenuIn, menu_id: uuid.UUID) -> Row[Any]:
        submenu_obj = Submenu(
            id=uuid.uuid4(),
            title=submenu.title,
            description=submenu.description,
            menu_id=menu_id,
        )
        self.session.add(submenu_obj)
        await self.session.commit()

        return await self.get_by_id_with_counts(submenu_obj.id)

    async def update(self, submenu_id: uuid.UUID, submenu: schemas.SubmenuIn) -> Row[Any] | None:
        submenu_obj = await self.get_by_id(submenu_id)

        if not submenu_obj:
            return None

        submenu_obj.title = submenu.title
        submenu_obj.description = submenu.description
        await self.session.commit()

        return await self.get_by_id_with_counts(submenu_obj.id)

    async def delete(self, submenu_id: uuid.UUID) -> bool:
        try:
            submenu = await self.get_by_id(submenu_id)
            await self.session.delete(submenu)
            await self.session.commit()

            return True
        except UnmappedInstanceError:
            return False

    async def get(self, menu_id: uuid.UUID) -> Sequence[Row[Any]]:
        res = await self.session.execute(
            select(
                Submenu,
                func.count(func.distinct(Dish.id)).label('dishes_count')
            )
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .where(Submenu.menu_id == menu_id)
            .group_by(Submenu.id, Submenu.title, Submenu.description)
        )

        return res.fetchall()

    async def get_by_id(self, submenu_id: uuid.UUID) -> Submenu:
        res = await self.session.execute(
            select(Submenu)
            .where(Submenu.id == submenu_id)
        )

        return res.scalars().one_or_none()

    async def get_by_title(self, title: str) -> Submenu:
        res = await self.session.execute(
            select(Submenu)
            .where(Submenu.title == title)
        )

        return res.scalars().one_or_none()

    async def get_by_id_with_counts(self, submenu_id: uuid.UUID) -> Row[Any]:
        res = await self.session.execute(
            select(
                Submenu,
                func.count(func.distinct(Dish.id)).label('dishes_count')
            )
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .where(Submenu.id == submenu_id)
            .group_by(Submenu.id, Submenu.title, Submenu.description)
        )

        return res.fetchone()
