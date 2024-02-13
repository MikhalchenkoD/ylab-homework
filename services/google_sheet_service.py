from parsers.google_sheet_parser import GoogleSheetsParser
from repositories.google_sheets_repository import GoogleSheetsRepository


class GoogleSheetService:
    def __init__(self):
        self.google_sheets_repository = GoogleSheetsRepository()
        self.parser = GoogleSheetsParser()

    async def get_dish_data_by_title(self, title: str):
        data = await self.google_sheets_repository.get_data()
        dishes = await self.parser.parse_dish_data(data)

        for dish in dishes:
            if dish['title'] == title:
                return dish
