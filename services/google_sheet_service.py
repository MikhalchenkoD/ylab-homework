from parsers.google_sheet_parser import GoogleSheetsParser
from repositories.google_sheets_repository import GoogleSheetsRepository
from repositories.redis_repository import RedisRepository


class GoogleSheetService:
    def __init__(self):
        self.google_sheets_repository = GoogleSheetsRepository()
        self.parser = GoogleSheetsParser()
        self.redis = RedisRepository()

    async def get_dish_data_by_title(self, title: str):
        dishes = await self.redis.get('dishes_data_from_google_sheet')

        if not dishes:
            data = await self.google_sheets_repository.get_data()
            dishes = await self.parser.parse_dish_data(data)

            await self.redis.save('dishes_data_from_google_sheet', value=dishes)

        for dish in dishes:
            if dish['title'] == title:
                return dish
