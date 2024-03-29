from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_async_session
from database.models import Dish
from services.dish_service import DishService
from utils import schemas

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
    responses={404: {'model': schemas.NotFoundError}}
)
async def get_dish_by_id(
        menu_id: UUID, submenu_id: UUID, dish_id: UUID, session: AsyncSession = Depends(get_async_session)
) -> Dish:
    return await DishService(session).get_by_id(menu_id, submenu_id, dish_id)


@dishes_router.post(
    '/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=schemas.DishOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_dish(
        background_tasks: BackgroundTasks,
        dish: schemas.DishIn,
        menu_id: UUID,
        submenu_id: UUID,
        session: AsyncSession = Depends(get_async_session),
) -> Dish:
    return await DishService(session).create(background_tasks, dish, menu_id, submenu_id)


@dishes_router.patch(
    '/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=schemas.DishOut,
    responses={404: {'model': schemas.NotFoundError}}
)
async def update_dish_by_id(
        dish: schemas.DishIn,
        background_tasks: BackgroundTasks,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        session: AsyncSession = Depends(get_async_session),
) -> Dish:
    return await DishService(session).update(background_tasks, dish, menu_id, dish_id)


@dishes_router.delete('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=schemas.OutAfterDelete, responses={404: {'model': schemas.NotFoundError}})
async def delete_dish_by_id(
        menu_id: UUID, background_tasks: BackgroundTasks, submenu_id: UUID, dish_id: UUID, session: AsyncSession = Depends(get_async_session)
) -> schemas.OutAfterDelete:
    return await DishService(session).delete(background_tasks, menu_id, dish_id)
