import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from database.models import Menu, Submenu
from main import app, BASE_API_URL
import utils.schemas as schemas
from typing import List, Sequence
from database.database import get_async_session
from fastapi import HTTPException, status


@app.get(BASE_API_URL + "menus", response_model=List[schemas.MenuOut])
async def get_list_menus(session: AsyncSession = Depends(get_async_session)) -> Sequence[Menu]:
    res = await session.execute(select(Menu).options(selectinload(Menu.submenus)))
    return res.scalars().all()


@app.get(BASE_API_URL + "menus/{menu_id}", response_model=schemas.MenuOut)
async def get_menu_by_id(menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(
        select(Menu)
        .options(selectinload(Menu.submenus).joinedload(Submenu.dishes))
        .where(Menu.id == menu_id)
    )
    menu = res.scalars().one_or_none()
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")
    return menu


@app.post(
    BASE_API_URL + "menus",
    response_model=schemas.MenuOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_menu(
        menu: schemas.MenuIn, session: AsyncSession = Depends(get_async_session)
) -> Menu:
    new_menu = Menu(id=uuid.uuid4(), title=menu.title, description=menu.description)
    session.add(new_menu)
    await session.commit()

    res = await session.execute(
        select(Menu).options(selectinload(Menu.submenus)).where(Menu.id == new_menu.id)
    )
    return res.scalars().one_or_none()


@app.patch(BASE_API_URL + "menus/{menu_id}", response_model=schemas.MenuOut)
async def update_menu_by_id(
        menu: schemas.MenuIn, menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)
) -> Menu:
    res = await session.execute(
        select(Menu)
        .options(selectinload(Menu.submenus).joinedload(Submenu.dishes))
        .where(Menu.id == menu_id)
    )
    result = res.scalars().one_or_none()
    result.title = menu.title
    result.description = menu.description

    await session.commit()

    return result


@app.delete(BASE_API_URL + "menus/{menu_id}")
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
