import uuid
from typing import List, Sequence

from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.database import get_async_session
from database.models import Submenu, Dish
from utils import schemas

submenus_router = APIRouter(prefix=f"/menus", tags=["Submenu"])


@submenus_router.get(
    "/{menu_id}/submenus", response_model=List[schemas.SubmenuOut]
)
async def get_list_submenus(
        menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)
) -> List[schemas.SubmenuOut]:
    res = await session.execute(
        select(
            Submenu,
            func.count(func.distinct(Dish.id)).label("dishes_count")
        )
        .outerjoin(Dish, Submenu.id == Dish.submenu_id)
        .group_by(Submenu.id, Submenu.title, Submenu.description)
    )

    result = res.fetchall()

    result_submenus = []
    for submenu_obj, dishes_count in result:
        submenu_out = schemas.SubmenuOut(
            id=submenu_obj.id,
            title=submenu_obj.title,
            description=submenu_obj.description,
            dishes_count=dishes_count
        )
        result_submenus.append(submenu_out)

    return result_submenus


@submenus_router.get(
    "/{menu_id}/submenus/{submenu_id}",
    response_model=schemas.SubmenuOut,
)
async def get_submenu_by_id(
        menu_id: uuid.UUID, submenu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)
) -> schemas.SubmenuOut:
    res = await session.execute(
        select(
            Submenu,
            func.count(func.distinct(Dish.id)).label("dishes_count")
        )
        .outerjoin(Dish, Submenu.id == Dish.submenu_id)
        .where(Submenu.menu_id == menu_id, Submenu.id == submenu_id)
        .group_by(Submenu.id, Submenu.title, Submenu.description)
    )

    result = res.fetchone()

    if result:
        submenu_obj, dishes_count = result
        submenu_out = schemas.SubmenuOut(
            id=submenu_obj.id,
            title=submenu_obj.title,
            description=submenu_obj.description,
            dishes_count=dishes_count
        )

        return submenu_out

    raise HTTPException(status_code=404, detail="submenu not found")



@submenus_router.post(
    "/{menu_id}/submenus",
    response_model=schemas.SubmenuOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_submenu(
        submenu: schemas.SubmenuIn,
        menu_id: uuid.UUID,
        session: AsyncSession = Depends(get_async_session),
) -> schemas.SubmenuOut:
    new_menu = Submenu(
        id=uuid.uuid4(),
        title=submenu.title,
        description=submenu.description,
        menu_id=menu_id,
    )
    session.add(new_menu)
    await session.commit()

    res = await session.execute(
        select(
            Submenu,
            func.count(func.distinct(Dish.id)).label("dishes_count")
        )
        .outerjoin(Dish, Submenu.id == Dish.submenu_id)
        .where(Submenu.menu_id == menu_id, Submenu.id == new_menu.id)
        .group_by(Submenu.id, Submenu.title, Submenu.description)
    )

    result = res.fetchone()

    if result:
        submenu_obj, dishes_count = result
        submenu_out = schemas.SubmenuOut(
            id=submenu_obj.id,
            title=submenu_obj.title,
            description=submenu_obj.description,
            dishes_count=dishes_count
        )

        return submenu_out


@submenus_router.patch(
    "/{menu_id}/submenus/{submenu_id}",
    response_model=schemas.SubmenuOut,
)
async def update_submenu_by_id(
        submenu: schemas.SubmenuIn,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        session: AsyncSession = Depends(get_async_session),
) -> schemas.SubmenuOut:
    res = await session.execute(
        select(
            Submenu,
            func.count(func.distinct(Dish.id)).label("dishes_count")
        )
        .outerjoin(Dish, Submenu.id == Dish.submenu_id)
        .where(Submenu.menu_id == menu_id, Submenu.id == submenu_id)
        .group_by(Submenu.id, Submenu.title, Submenu.description)
    )

    result = res.fetchone()

    if result:
        submenu_obj, dishes_count = result
        submenu_obj.title = submenu.title
        submenu_obj.description = submenu.description
        await session.commit()

        submenu_out = schemas.SubmenuOut(
            id=submenu_obj.id,
            title=submenu_obj.title,
            description=submenu_obj.description,
            dishes_count=dishes_count
        )

        return submenu_out


@submenus_router.delete("/{menu_id}/submenus/{submenu_id}")
async def delete_submenu_by_id(
        menu_id: uuid.UUID, submenu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)
) -> dict:
    res = await session.execute(
        select(Submenu).where(Submenu.menu_id == menu_id, Submenu.id == submenu_id)
    )
    result = res.scalars().one_or_none()

    await session.delete(result)
    await session.commit()

    return {
        "status": True,
        "message": "The submenu has been deleted"
    }
