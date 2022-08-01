import datetime
import math
import requests
from lxml import etree
import pandas as pd
import gspread
from config import PARSING_RANGE


def get_usd_exchange_rate() -> float:
    url = 'https://www.cbr.ru/scripts/XML_daily.asp?'
    request = requests.get(url)
    tree = etree.XML(request.content)
    valute_node = tree.xpath('//Valute[@ID = "R01235"]')[0]
    nominal = float(valute_node.find('Nominal').text.replace(',', "."))
    value = float(valute_node.find('Value').text.replace(',', "."))
    return nominal * value


def string_to_date(date_string: str) -> datetime.date:
    return datetime.datetime.strptime(date_string, '%d.%m.%Y').date()


def get_sheet_padding_data(work_sheet: gspread.Worksheet, padding: int) -> pd.DataFrame:
    data = work_sheet.get(f'A{(PARSING_RANGE * (padding - 1)) + 1}:D{PARSING_RANGE * padding}')
    dataframe = pd.DataFrame(data if padding != 1 else data[1:])
    return dataframe


def get_sheet_data(work_sheet: gspread.Worksheet) -> pd.DataFrame:
    padding_count = math.ceil(work_sheet.row_count / PARSING_RANGE)
    data = []
    for padding in range(1, padding_count + 1):
        data.append(get_sheet_padding_data(work_sheet, padding))
    return pd.concat(data, ignore_index=True)
