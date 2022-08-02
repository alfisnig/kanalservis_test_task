import time
import pandas as pd
from sheetparser import get_sheet_data, get_usd_exchange_rate, string_to_date
from sheetparser import get_work_sheet
from db import delete_all_orders, get_orders, add_orders, update_orders, get_all_order_nums, delete_orders
from config import SHEET_MONITORING_DELAY


def confirm_deleted_orders(sheet_orders_column: pd.Series):
    """Удаляет из базы заказы, которых на момент парсинга не оказалось в гугл таблице"""
    order_nums = get_all_order_nums()
    order_nums = pd.DataFrame(order_nums)

    need_to_delete_orders = []
    for order_num in order_nums.itertuples(index=False):
        order_num = order_num[0]
        if order_num not in sheet_orders_column.values:
            need_to_delete_orders.append(int(order_num))

    delete_orders(need_to_delete_orders)


def sheet_monitoring():
    # берём из таблицы во вкладке Data и удаляем пустые строки из полученного DataFrame
    work_sheet = get_work_sheet('Data')
    sheet_rows = get_sheet_data(work_sheet).dropna()
    # если все строки оказались пустыми, удалить все записи из базы данных
    if sheet_rows.size == 0:
        delete_all_orders()
        return None
    sheet_orders_column = sheet_rows[1]
    # получение заказов из БД по их order_num
    db_rows = get_orders(sheet_orders_column)
    # получение курса доллара
    usd_rate = get_usd_exchange_rate()
    new_orders = []
    updates = []
    for sheet_row, db_row in zip(sheet_rows.itertuples(index=False), db_rows):
        number, order_number, price, delivery_time = sheet_row
        number, order_number, price = int(number), int(order_number), float(price)
        # если по конкретному order_num в БД не нашлось строки, то добавляем её в БД
        if db_row is None:
            delivery_time = string_to_date(delivery_time)
            price_rub = price * usd_rate
            new_orders.append((number, order_number, price, price_rub, delivery_time, usd_rate))
        # если строка есть в БД, сравниваем была ли она изменена. Если да, изменяем существующую строку в БД
        elif (number, order_number, price, delivery_time) != db_row:
            delivery_time = string_to_date(delivery_time)
            updates.append((number, order_number, price, delivery_time))
    # выполняем запросы на добавление, изменение, удаление заказов
    add_orders(new_orders)
    update_orders(updates)
    confirm_deleted_orders(pd.Series(sheet_orders_column, dtype='int'))


def start_sheet_monitoring():
    while True:
        try:
            sheet_monitoring()
        except Exception as e:
            print(e)
        time.sleep(SHEET_MONITORING_DELAY)


if __name__ == '__main__':
    start_sheet_monitoring()
