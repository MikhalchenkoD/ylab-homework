from typing import Any, Sequence

from sqlalchemy import Row

from repositories.discount_repository import DiscountRepository
from services.google_sheet_service import GoogleSheetService
from utils import schemas


class MenuConverter:
    async def convert_list_menus(self, menus: Sequence[Row[Any]]) -> list[schemas.MenuOut]:
        menus_result = []
        for menu, submenus_count, dishes_count in menus:
            menu_out = schemas.MenuOut(
                id=menu.id,
                title=menu.title,
                description=menu.description,
                submenus_count=submenus_count,
                dishes_count=dishes_count
            )
            menus_result.append(menu_out)

        return menus_result

    async def convert_menu(self, menu: Row[Any]) -> schemas.MenuOut:
        menu_obj, submenus_count, dishes_count = menu
        menu_out = schemas.MenuOut(
            id=menu_obj.id,
            title=menu_obj.title,
            description=menu_obj.description,
            submenus_count=submenus_count,
            dishes_count=dishes_count
        )
        return menu_out

    async def convert_menu_with_submenus_and_dishes(
            self, menus: Sequence[Row[Any]]
    ) -> list[schemas.MenuOutWithSubmenusAndDishes]:
        menus_result = []

        for menu_row in menus:
            menu = menu_row[0]
            menu_out = schemas.MenuOutWithSubmenusAndDishes(
                id=menu.id,
                title=menu.title,
                description=menu.description,
                submenus=[],
                dishes=[]
            )

            for submenu in menu.submenus:

                for dish in submenu.dishes:
                    dish_data = await GoogleSheetService().get_dish_data_by_title(dish.title)

                    if dish_data:
                        dish = await DiscountRepository().set_discount_for_dish(dish, dish_data['discount'])

                    menu_out.dishes.append(dish)

                menu_out.submenus.append(submenu)

            menus_result.append(menu_out)

        return menus_result
