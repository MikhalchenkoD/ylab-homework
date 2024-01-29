import uuid

from fastapi import Depends, APIRouter
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Menu, Submenu, Dish
from utils import schemas
from typing import List
from database.database import get_async_session
from fastapi import HTTPException, status

menus_router = APIRouter(prefix=f"/menus", tags=["Menu"])


@menus_router.get("/", response_model=List[schemas.MenuOut])
async def get_list_menus(session: AsyncSession = Depends(get_async_session)) -> List[schemas.MenuOut]:
    res = await session.execute(
        select(
            Menu,
            func.count(func.distinct(Submenu.id)).label("submenus_count"),
            func.count(func.distinct(Dish.id)).label("dishes_count")
        )
        .outerjoin(Submenu, Menu.id == Submenu.menu_id)
        .outerjoin(Dish, Submenu.id == Dish.submenu_id)
        .group_by(Menu.id, Menu.title, Menu.description)
    )

    result = res.fetchall()

    result_menus = []
    for menu, submenus_count, dishes_count in result:
        menu_out = schemas.MenuOut(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=submenus_count,
            dishes_count=dishes_count
        )
        result_menus.append(menu_out)

    return result_menus


@menus_router.get("/{menu_id}", response_model=schemas.MenuOut)
async def get_menu_by_id(menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(
        select(
            Menu,
            func.count(func.distinct(Submenu.id)).label("submenus_count"),
            func.count(func.distinct(Dish.id)).label("dishes_count")
        )
        .outerjoin(Submenu, Menu.id == Submenu.menu_id)
        .outerjoin(Dish, Submenu.id == Dish.submenu_id)
        .where(Menu.id == menu_id)
        .group_by(Menu.id, Menu.title, Menu.description)
    )

    result = res.fetchone()

    if result:
        menu_obj, submenus_count, dishes_count = result
        menu_out = schemas.MenuOut(
            id=menu_obj.id,
            title=menu_obj.title,
            description=menu_obj.description,
            submenus_count=submenus_count,
            dishes_count=dishes_count
        )
        return menu_out

    raise HTTPException(status_code=404, detail="menu not found")


@menus_router.post(
    "/",
    response_model=schemas.MenuOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_menu(
        menu: schemas.MenuIn, session: AsyncSession = Depends(get_async_session)
) -> schemas.MenuOut:
    new_menu = Menu(id=uuid.uuid4(), title=menu.title, description=menu.description)
    session.add(new_menu)
    await session.commit()

    res = await session.execute(
        select(
            Menu,
            func.count(func.distinct(Submenu.id)).label("submenus_count"),
            func.count(func.distinct(Dish.id)).label("dishes_count")
        )
        .outerjoin(Submenu, Menu.id == Submenu.menu_id)
        .outerjoin(Dish, Submenu.id == Dish.submenu_id)
        .where(Menu.id == new_menu.id)
        .group_by(Menu.id, Menu.title, Menu.description)
    )

    result = res.fetchone()

    if result:
        menu_obj, submenus_count, dishes_count = result
        menu_out = schemas.MenuOut(
            id=menu_obj.id,
            title=menu_obj.title,
            description=menu_obj.description,
            submenus_count=submenus_count,
            dishes_count=dishes_count
        )
        return menu_out


@menus_router.patch("/{menu_id}", response_model=schemas.MenuOut)
async def update_menu_by_id(
        menu: schemas.MenuIn, menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)
) -> schemas.MenuOut:
    res = await session.execute(
        select(
            Menu,
            func.count(func.distinct(Submenu.id)).label("submenus_count"),
            func.count(func.distinct(Dish.id)).label("dishes_count")
        )
        .outerjoin(Submenu, Menu.id == Submenu.menu_id)
        .outerjoin(Dish, Submenu.id == Dish.submenu_id)
        .where(Menu.id == menu_id)
        .group_by(Menu.id, Menu.title, Menu.description)
    )

    result = res.fetchone()

    if result:
        menu_obj, submenus_count, dishes_count = result
        menu_obj.title = menu.title
        menu_obj.description = menu.description
        await session.commit()

        menu_out = schemas.MenuOut(
            id=menu_obj.id,
            title=menu_obj.title,
            description=menu_obj.description,
            submenus_count=submenus_count,
            dishes_count=dishes_count
        )
        return menu_out


@menus_router.delete("/{menu_id}")
async def delete_menu_by_id(
        menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)
) -> dict:
    res = await session.execute(select(Menu).where(Menu.id == menu_id))
    result = res.scalars().one_or_none()

    await session.delete(result)
    await session.commit()

    return {
        "status": True,
        "message": "The menu has been deleted"
    }
