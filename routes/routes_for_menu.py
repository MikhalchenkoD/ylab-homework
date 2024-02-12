import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_async_session
from services.menu_service import MenuService
from utils import schemas

menus_router = APIRouter(prefix='/menus', tags=['Menu'])


@menus_router.get('/', response_model=list[schemas.MenuOut])
async def get_list_menus(session: AsyncSession = Depends(get_async_session)) -> list[schemas.MenuOut]:
    return await MenuService(session).get()


@menus_router.get('/all', response_model=list[schemas.MenuOutWithSubmenusAndDishes])
async def get_list_menus_with_submenus_and_dishes(session: AsyncSession = Depends(get_async_session)) -> list[schemas.MenuOutWithSubmenusAndDishes]:
    return await MenuService(session).get_menus_with_submenus_and_dishes()


@menus_router.get('/{menu_id}', response_model=schemas.MenuOut, responses={404: {'model': schemas.NotFoundError}})
async def get_menu_by_id(menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)) -> schemas.MenuOut:
    return await MenuService(session).get_by_id(menu_id)


@menus_router.post(
    '/',
    response_model=schemas.MenuOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_menu(
        background_tasks: BackgroundTasks, menu: schemas.MenuIn, session: AsyncSession = Depends(get_async_session)
) -> schemas.MenuOut:
    return await MenuService(session).create(background_tasks, menu)


@menus_router.patch('/{menu_id}', response_model=schemas.MenuOut, responses={404: {'model': schemas.NotFoundError}})
async def update_menu_by_id(
        background_tasks: BackgroundTasks, menu: schemas.MenuIn, menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)
) -> schemas.MenuOut:
    return await MenuService(session).update(background_tasks, menu, menu_id)


@menus_router.delete('/{menu_id}', response_model=schemas.OutAfterDelete,
                     responses={404: {'model': schemas.NotFoundError}})
async def delete_menu_by_id(
        background_tasks: BackgroundTasks, menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)
) -> schemas.OutAfterDelete:
    return await MenuService(session).delete(background_tasks, menu_id)
