import gspread
from config import CREDENTIALS_FILE_PATH, SPREADSHEET_ID


def get_sheet() -> gspread.Spreadsheet:
    service_account = gspread.service_account(CREDENTIALS_FILE_PATH)
    sheet = service_account.open_by_key(SPREADSHEET_ID)
    return sheet


def get_work_sheet(title: str) -> gspread.Worksheet:
    sheet = get_sheet()
    work_sheet = sheet.worksheet(title)
    return work_sheet
