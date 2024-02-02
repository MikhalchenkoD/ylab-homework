from typing import Sequence, Any

from sqlalchemy import Row

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
