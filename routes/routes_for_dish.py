from uuid import UUID, uuid4
from typing import List, Sequence

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_async_session
from main import app, BASE_API_URL
from utils import schemas
from database.models import Dish, Submenu


@app.get(
    BASE_API_URL + "menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=List[schemas.DishOut],
)
async def get_list_dishes(
        menu_id: UUID, submenu_id: UUID, session: AsyncSession = Depends(get_async_session)
) -> Sequence[Dish]:
    res = await session.execute(
        select(Dish)
        .join(Submenu)
        .where(Submenu.menu_id == menu_id, Dish.submenu_id == submenu_id)
    )
    return res.scalars().all()


@app.get(
    BASE_API_URL + "menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=schemas.DishOut,
)
async def get_dish_by_id(
        menu_id: UUID, submenu_id: UUID, dish_id: UUID, session: AsyncSession = Depends(get_async_session)
) -> Dish:
    res = await session.execute(
        select(Dish)
        .join(Submenu)
        .where(
            Submenu.menu_id == menu_id,
            Dish.submenu_id == submenu_id,
            Dish.id == dish_id,
        )
    )
    dish = res.scalars().one_or_none()
    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")
    return dish


@app.post(
    BASE_API_URL + "menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=schemas.DishOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_dish(
        dish: schemas.DishIn,
        menu_id: UUID,
        submenu_id: UUID,
        session: AsyncSession = Depends(get_async_session),
) -> Dish:
    res = await session.execute(
        select(Submenu).where(Submenu.menu_id == menu_id, Submenu.id == submenu_id)
    )
    submenu = res.scalars().one_or_none()
    new_dish = Dish(
        id=uuid4(),
        title=dish.title,
        description=dish.description,
        price=dish.price,
        submenu_id=submenu.id,
    )
    session.add(new_dish)
    await session.commit()
    return new_dish


@app.patch(
    BASE_API_URL + "menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=schemas.DishOut,
)
async def update_dish_by_id(
        dish: schemas.DishIn,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        session: AsyncSession = Depends(get_async_session),
) -> Dish:
    res = await session.execute(
        select(Dish)
        .join(Submenu)
        .where(
            Submenu.menu_id == menu_id,
            Dish.submenu_id == submenu_id,
            Dish.id == dish_id,
        )
    )
    result = res.scalars().one_or_none()
    result.title = dish.title
    result.description = dish.description
    result.price = dish.price
    await session.commit()

    return result


@app.delete(BASE_API_URL + "menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def delete_dish_by_id(
        menu_id: UUID, submenu_id: UUID, dish_id: UUID, session: AsyncSession = Depends(get_async_session)
) -> dict:
    res = await session.execute(
        select(Dish)
        .join(Submenu)
        .where(
            Submenu.menu_id == menu_id,
            Dish.submenu_id == submenu_id,
            Dish.id == dish_id,
        )
    )
    result = res.scalars().one_or_none()

    await session.delete(result)
    await session.commit()

    return {
        "status": True,
        "message": "The dish has been deleted"
    }
