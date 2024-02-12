from sqlalchemy.ext.asyncio import AsyncSession

from parsers.google_sheet_parser import GoogleSheetsParser
from repositories.dish_repository import DishRepository
from repositories.google_sheets_repository import GoogleSheetsRepository
from repositories.menu_repository import MenuRepository
from repositories.redis_repository import RedisRepository
from repositories.submenu_repository import SubmenuRepository
from utils import schemas


class TaskService:
    def __init__(self, session: AsyncSession):
        self.google_sheets_repository = GoogleSheetsRepository()
        self.parser = GoogleSheetsParser()
        self.session = session
        self.menu_repository = MenuRepository(session)
        self.submenu_repository = SubmenuRepository(session)
        self.dish_repository = DishRepository(session)
        self.redis = RedisRepository()

    async def check_data(self):
        data = await self.google_sheets_repository.get_data()
        parsed_data = await self.parser.parse_data(data)
        for menu_item in parsed_data:
            menu = await self.menu_repository.get_by_title(menu_item['title'])
            menu_id = None
            submenu_id = None

            if not menu:
                menu_data = schemas.MenuIn(title=menu_item['title'], description=menu_item['description'])
                created_menu = await self.menu_repository.create(menu_data)

                await self.redis.delete('menus_list')

                menu_id = created_menu[0].id

            elif menu.title != menu_item['title'] or menu.description != menu_item['description']:
                menu_data = schemas.MenuIn(title=menu_item['title'], description=menu_item['description'])
                updated_menu = await self.menu_repository.update(menu.id, menu_data)

                await self.redis.delete_parents_and_children_keys(menu_id)

                menu_id = updated_menu[0].id

            for submenu_item in menu_item['submenus']:
                submenu = await self.submenu_repository.get_by_title(submenu_item['title'])

                if not submenu:
                    submenu_data = schemas.SubmenuIn(title=submenu_item['title'],
                                                     description=submenu_item['description'])
                    created_submenu = await self.submenu_repository.create(submenu_data, menu_id)

                    await self.redis.delete_parents_and_children_keys(menu_id)

                    submenu_id = created_submenu[0].id

                elif submenu.title != submenu_item['title'] or submenu.description != submenu_item['description']:
                    submenu_data = schemas.SubmenuIn(title=submenu_item['title'],
                                                     description=submenu_item['description'])
                    updated_menu = await self.submenu_repository.update(submenu.id, submenu_data)

                    await self.redis.delete_parents_and_children_keys(menu_id)

                    submenu_id = updated_menu[0].id

                for dish_item in submenu_item['dishes']:
                    dish = await self.dish_repository.get_by_title(dish_item['title'])

                    if not dish:
                        dish_data = schemas.DishIn(title=dish_item['title'],
                                                   description=dish_item['description'], price=dish_item['price'])
                        await self.dish_repository.create(dish_data, submenu_id)

                        await self.redis.delete_parents_and_children_keys(menu_id)

                    elif dish.title != dish_item['title'] or dish.description != dish_item[
                            'description'] or dish.price != dish_item['price']:
                        dish_data = schemas.DishIn(title=dish_item['title'],
                                                   description=dish_item['description'], price=dish_item['price'])
                        await self.dish_repository.update(dish.id, dish_data)

                        await self.redis.delete_parents_and_children_keys(menu_id)
