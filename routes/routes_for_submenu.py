import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_async_session
from services.submenu_service import SubmenuService
from utils import schemas

submenus_router = APIRouter(prefix='/menus', tags=['Submenu'])


@submenus_router.get(
    '/{menu_id}/submenus', response_model=list[schemas.SubmenuOut]
)
async def get_list_submenus(
        menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)
) -> list[schemas.SubmenuOut]:
    return await SubmenuService(session).get(menu_id)


@submenus_router.get(
    '/{menu_id}/submenus/{submenu_id}',
    response_model=schemas.SubmenuOut,
    responses={404: {'model': schemas.NotFoundError}}
)
async def get_submenu_by_id(
        menu_id: uuid.UUID, submenu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)
) -> schemas.SubmenuOut:
    return await SubmenuService(session).get_by_id(menu_id, submenu_id)


@submenus_router.post(
    '/{menu_id}/submenus',
    response_model=schemas.SubmenuOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_submenu(
        background_tasks: BackgroundTasks,
        submenu: schemas.SubmenuIn,
        menu_id: uuid.UUID,
        session: AsyncSession = Depends(get_async_session),
) -> schemas.SubmenuOut:
    return await SubmenuService(session).create(background_tasks, submenu, menu_id)


@submenus_router.patch(
    '/{menu_id}/submenus/{submenu_id}',
    response_model=schemas.SubmenuOut,
    responses={404: {'model': schemas.NotFoundError}}
)
async def update_submenu_by_id(
        background_tasks: BackgroundTasks,
        submenu: schemas.SubmenuIn,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        session: AsyncSession = Depends(get_async_session),
) -> schemas.SubmenuOut:
    return await SubmenuService(session).update(background_tasks, submenu, menu_id, submenu_id)


@submenus_router.delete('/{menu_id}/submenus/{submenu_id}', response_model=schemas.OutAfterDelete, responses={404: {'model': schemas.NotFoundError}})
async def delete_submenu_by_id(
        background_tasks: BackgroundTasks, menu_id: uuid.UUID, submenu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)
) -> schemas.OutAfterDelete:
    return await SubmenuService(session).delete(background_tasks, menu_id, submenu_id)
