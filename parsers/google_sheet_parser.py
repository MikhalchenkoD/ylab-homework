class GoogleSheetsParser:
    async def parse_data(self, data):
        result = []
        for i in data:
            if i[0]:
                menu = {
                    'title': i[1],
                    'description': i[2],
                    'submenus': [],
                }
                result.append(menu)
            elif not i[0] and i[1]:
                submenu = {
                    'title': i[2],
                    'description': i[3],
                    'dishes': []
                }
                result[-1]['submenus'].append(submenu)
            elif not i[1] and i[2]:
                dish = {
                    'title': i[3],
                    'description': i[4],
                    'price': i[5],
                }
                result[-1]['submenus'][-1]['dishes'].append(dish)

        return result
