class GoogleSheetsParser:

    async def parse_data(self, data: list[list]) -> list[dict]:
        result = []
        for i in data:
            if i[0]:
                menu = {
                    'id': i[0],
                    'title': i[1],
                    'description': i[2],
                    'submenus': [],
                }
                result.append(menu)
            elif not i[0] and i[1]:
                submenu = {
                    'id': i[1],
                    'title': i[2],
                    'description': i[3],
                    'dishes': []
                }
                result[-1]['submenus'].append(submenu)
            elif not i[1] and i[2]:
                dish = {
                    'id': i[2],
                    'title': i[3],
                    'description': i[4],
                    'price': i[5],
                }
                result[-1]['submenus'][-1]['dishes'].append(dish)

        return result

    async def parse_dish_data(self, data: list[list]) -> list[dict]:
        result = []
        for i in data:
            if not i[1] and i[2]:
                dish = {
                    'id': i[2],
                    'title': i[3],
                    'description': i[4],
                    'price': i[5],
                    'discount': int(i[6]) if len(i) == 7 else 0
                }
                result.append(dish)

        return result
