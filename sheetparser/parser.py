from typing import Iterable
import datetime
import time
import math
import requests
from lxml import etree
import pandas as pd
import gspread
from config import PARSING_RANGE
from connection import get_work_sheet
from db import check_orders, add_order, update_order


def usd_to_rub(usd_price: float, date: datetime.date = None) -> int:
    if date is None:
        url = 'https://www.cbr.ru/scripts/XML_daily.asp?'
    else:
        url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date.strftime("%d/%m/%Y")}'
    request = requests.get(url)
    tree = etree.XML(request.content)
    valute_node = tree.xpath('//Valute[@ID = "R01235"]')[0]
    nominal = float(valute_node.find('Nominal').text.replace(',', "."))
    value = float(valute_node.find('Value').text.replace(',', "."))
    return nominal * value * usd_price


def string_to_date(date_string: str) -> datetime.date:
    return datetime.datetime.strptime(date_string, '%d.%m.%Y').date()


def add_new_record(number: int, order_number: int, price: float, delivery_time: datetime.date):
    price_rub = usd_to_rub(float(price))
    delivery_time = string_to_date(delivery_time)
    add_order(number, order_number, price, price_rub, delivery_time)


def get_sheet_data(work_sheet: gspread.Worksheet, padding: int) -> pd.DataFrame:
    data = work_sheet.get(f'A1:D{PARSING_RANGE * padding}')
    dataframe = pd.DataFrame(data[1:])
    return dataframe


def compare_and_update(sheet_row, db_row):
    if sheet_row != db_row:
        number, order_number, price, delivery_time = sheet_row
        delivery_time = string_to_date(delivery_time)
        price_rub = usd_to_rub(float(price), date=delivery_time)
        update_order(number, order_number, price, price_rub, delivery_time)


def sheet_monitoring():
    work_sheet = get_work_sheet('Data')
    padding_count = math.ceil(work_sheet.row_count / PARSING_RANGE)

    for padding in range(1, padding_count + 1):
        data = get_sheet_data(work_sheet, padding)
        db_rows = check_orders(data[1])
        for sheet_row, db_row in zip(data.itertuples(index=False), db_rows):
            number, order_number, price, delivery_time = sheet_row
            number, order_number, price = int(number), int(order_number), float(price)
            if db_row is None:
                add_new_record(number, order_number, price, delivery_time)
            else:
                compare_and_update((number, order_number, price, delivery_time), db_row)


def start_monitoring():
    while True:
        try:
            sheet_monitoring()
        except Exception as e:
            print(e)
        time.sleep(30)


if __name__ == '__main__':
    start_monitoring()
