import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from converters.menu_converter import MenuConverter
from repositories.menu_repository import MenuRepository
from repositories.redis_repository import RedisRepository
from utils import schemas


class MenuService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.converter = MenuConverter()
        self.repository = MenuRepository(self.session)
        self.redis = RedisRepository()

    async def create(self, menu: schemas.MenuIn) -> schemas.MenuOut:
        created_menu = await self.repository.create(menu)
        converted_menu = await self.converter.convert_menu(created_menu)

        await self.redis.delete('menus_list')

        return converted_menu

    async def get(self) -> list[schemas.MenuOut]:
        menus_in_cache = await self.redis.get('menu_list')

        if menus_in_cache:
            return menus_in_cache

        menus = await self.repository.get()
        converted_menus = await self.converter.convert_list_menus(menus)

        await self.redis.save('menus_list', value=converted_menus)

        return converted_menus

    async def get_by_id(self, menu_id: uuid.UUID) -> schemas.MenuOut:
        menu_in_cache = await self.redis.get(menu_id)

        if menu_in_cache:
            return menu_in_cache

        menu = await self.repository.get_by_id_with_counts(menu_id)

        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')

        converted_menu = await self.converter.convert_menu(menu)

        await self.redis.save(menu_id, value=converted_menu)

        return converted_menu

    async def update(self, menu: schemas.MenuIn, menu_id: uuid.UUID) -> schemas.MenuOut:
        updated_menu = await self.repository.update(menu_id, menu)
        converted_menu = await self.converter.convert_menu(updated_menu)

        await self.redis.delete_parents_and_children_keys(menu_id)

        return converted_menu

    async def delete(self, menu_id: uuid.UUID) -> schemas.OutAfterDelete:
        await self.repository.delete(menu_id)

        await self.redis.delete_parents_and_children_keys(menu_id)

        return schemas.OutAfterDelete(status=True, message='The menu has been deleted')
