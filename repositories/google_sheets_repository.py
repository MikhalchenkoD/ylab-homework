import gspread


class GoogleSheetsRepository:
    async def get_data(self) -> list[list]:
        creds = gspread.service_account(filename='admin/swift-adviser-413809-eab9b0b5a6ca.json')
        sheet = creds .open('Menu').sheet1

        data = sheet .get()

        return data
