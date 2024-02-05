import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_async_session
from services.menu_service import MenuService
from utils import schemas

menus_router = APIRouter(prefix='/menus', tags=['Menu'])


@menus_router.get('/', response_model=list[schemas.MenuOut])
async def get_list_menus(session: AsyncSession = Depends(get_async_session)) -> list[schemas.MenuOut]:
    return await MenuService(session).get()


@menus_router.get('/{menu_id}', response_model=schemas.MenuOut, responses={404: {'model': schemas.NotFoundError}})
async def get_menu_by_id(menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)) -> schemas.MenuOut:
    return await MenuService(session).get_by_id(menu_id)


@menus_router.post(
    '/',
    response_model=schemas.MenuOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_menu(
        menu: schemas.MenuIn, session: AsyncSession = Depends(get_async_session)
) -> schemas.MenuOut:

    return await MenuService(session).create(menu)


@menus_router.patch('/{menu_id}', response_model=schemas.MenuOut)
async def update_menu_by_id(
        menu: schemas.MenuIn, menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)
) -> schemas.MenuOut:
    return await MenuService(session).update(menu, menu_id)


@menus_router.delete('/{menu_id}', response_model=schemas.OutAfterDelete)
async def delete_menu_by_id(
        menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)
) -> schemas.OutAfterDelete:
    return await MenuService(session).delete(menu_id)
