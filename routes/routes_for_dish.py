from uuid import UUID
from typing import Sequence

from fastapi import Depends, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from services.dish_service import DishService
from database.database import get_async_session
from utils import schemas
from database.models import Dish

dishes_router = APIRouter(prefix='/menus', tags=['Dish'])


@dishes_router.get(
    '/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=list[schemas.DishOut],
)
async def get_list_dishes(
        menu_id: UUID, submenu_id: UUID, session: AsyncSession = Depends(get_async_session)
) -> Sequence[Dish]:
    return await DishService(session).get(submenu_id)


@dishes_router.get(
    '/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=schemas.DishOut,
)
async def get_dish_by_id(
        menu_id: UUID, submenu_id: UUID, dish_id: UUID, session: AsyncSession = Depends(get_async_session)
) -> Dish:
    return await DishService(session).get_by_id(dish_id)


@dishes_router.post(
    '/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=schemas.DishOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_dish(
        dish: schemas.DishIn,
        menu_id: UUID,
        submenu_id: UUID,
        session: AsyncSession = Depends(get_async_session),
) -> Dish:
    return await DishService(session).create(dish, submenu_id)


@dishes_router.patch(
    '/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=schemas.DishOut,
)
async def update_dish_by_id(
        dish: schemas.DishIn,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        session: AsyncSession = Depends(get_async_session),
) -> Dish:
    return await DishService(session).update(dish, dish_id)


@dishes_router.delete('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=schemas.OutAfterDelete)
async def delete_dish_by_id(
        menu_id: UUID, submenu_id: UUID, dish_id: UUID, session: AsyncSession = Depends(get_async_session)
) -> schemas.OutAfterDelete:
    return await DishService(session).delete(dish_id)
