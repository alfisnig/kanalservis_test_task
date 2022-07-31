from typing import List
import datetime
import time
import math
import requests
from lxml import etree
import pandas as pd
import gspread
from config import PARSING_RANGE
from connection import get_work_sheet
from db import get_orders, add_orders, update_orders, get_all_order_nums, delete_orders, delete_all_orders


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


def confirm_deleted_orders(sheet_orders_column: pd.Series):
    order_nums = get_all_order_nums()
    order_nums = pd.DataFrame(order_nums)

    need_to_delete_orders = []
    for order_num in order_nums.itertuples(index=False):
        order_num = order_num[0]
        if order_num not in sheet_orders_column.values:
            need_to_delete_orders.append(int(order_num))

    delete_orders(need_to_delete_orders)


def sheet_monitoring():
    work_sheet = get_work_sheet('Data')
    sheet_rows = get_sheet_data(work_sheet).dropna()
    if sheet_rows.size == 0:
        delete_all_orders()
        return None
    sheet_orders_column = sheet_rows[1]
    db_rows = get_orders(sheet_orders_column)
    usd_rate = get_usd_exchange_rate()
    new_orders = []
    updates = []
    for sheet_row, db_row in zip(sheet_rows.itertuples(index=False), db_rows):
        number, order_number, price, delivery_time = sheet_row
        number, order_number, price = int(number), int(order_number), float(price)
        if db_row is None:
            delivery_time = string_to_date(delivery_time)
            price_rub = price * usd_rate
            new_orders.append((number, order_number, price, price_rub, delivery_time, usd_rate))
        elif (number, order_number, price, delivery_time) != db_row:
            delivery_time = string_to_date(delivery_time)
            updates.append((number, order_number, price, delivery_time))
    add_orders(new_orders)
    update_orders(updates)
    confirm_deleted_orders(pd.Series(sheet_orders_column, dtype="int"))


def start_monitoring():
    while True:
        try:
            sheet_monitoring()
        except Exception as e:
            print(e)
        time.sleep(30)


if __name__ == '__main__':
    start_monitoring()
