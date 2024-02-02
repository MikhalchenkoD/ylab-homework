from typing import Sequence, Any

from sqlalchemy import Row

from utils import schemas


class SubmenuConverter:
    async def convert_list_submenus(self, submenus: Sequence[Row[Any]]) -> list[schemas.SubmenuOut]:
        submenus_list = []
        for submenu_obj, dishes_count in submenus:
            submenu_out = schemas.SubmenuOut(
                id=submenu_obj.id,
                title=submenu_obj.title,
                description=submenu_obj.description,
                dishes_count=dishes_count
            )
            submenus_list.append(submenu_out)

        return submenus_list

    async def convert_menu(self, submenu: Row[Any]) -> schemas.SubmenuOut:
        submenu_obj, dishes_count = submenu
        submenu_out = schemas.SubmenuOut(
            id=submenu_obj.id,
            title=submenu_obj.title,
            description=submenu_obj.description,
            dishes_count=dishes_count
        )

        return submenu_out
