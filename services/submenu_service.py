import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from converters.submenu_converter import SubmenuConverter
from repositories.redis_repository import RedisRepository
from repositories.submenu_repository import SubmenuRepository
from utils import schemas
from utils.schemas import SubmenuOut


class SubmenuService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.converter = SubmenuConverter()
        self.repository = SubmenuRepository(self.session)
        self.redis = RedisRepository()

    async def create(self, submenu: schemas.SubmenuIn, menu_id: uuid.UUID) -> schemas.SubmenuOut:
        created_submenu = await self.repository.create(submenu, menu_id)
        converted_submenu = await self.converter.convert_menu(created_submenu)

        await self.redis.clear_all()

        return converted_submenu

    async def get(self, menu_id: uuid.UUID) -> list[schemas.SubmenuOut]:
        submenus_in_cache = await self.redis.get('submenus_list')

        if submenus_in_cache:
            return submenus_in_cache

        submenus = await self.repository.get(menu_id)
        converted_submenus = await self.converter.convert_list_submenus(submenus)

        await self.redis.save('submenus_list', converted_submenus)

        return converted_submenus

    async def get_by_id(self, submenu_id: uuid.UUID) -> SubmenuOut:
        submenu_in_cache = await self.redis.get(submenu_id)

        if submenu_in_cache:
            return submenu_in_cache

        submenu = await self.repository.get_by_id_with_counts(submenu_id)

        if not submenu:
            raise HTTPException(status_code=404, detail='submenu not found')

        converted_submenu = await self.converter.convert_menu(submenu)

        await self.redis.save(submenu_id, converted_submenu)

        return converted_submenu

    async def update(self, submenu: schemas.SubmenuIn, submenu_id: uuid.UUID) -> SubmenuOut:
        updated_submenu = await self.repository.update(submenu_id, submenu)
        converted_submenu = await self.converter.convert_menu(updated_submenu)

        await self.redis.clear_all()

        return converted_submenu

    async def delete(self, submenu_id: uuid.UUID) -> schemas.OutAfterDelete:
        await self.repository.delete(submenu_id)

        await self.redis.clear_all()

        return schemas.OutAfterDelete(status=True, message='The submenu has been deleted')
