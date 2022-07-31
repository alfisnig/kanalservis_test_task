import datetime
from psycopg2.extras import execute_values
from typing import List, Iterable
from config import DB_NAME
from .connection import get_cursor


def add_orders(orders: List[tuple]):
    if not orders:
        return None
    sql = ('INSERT INTO orders'
           '    (number, order_num, price, price_rub, delivery_time, usd_exchange_rate)'
           'VALUES %s')
    with get_cursor(DB_NAME) as cursor:
        execute_values(cursor, sql, orders)


def update_orders(orders: List[tuple]):
    if not orders:
        return None
    with get_cursor(DB_NAME) as cursor:
        for order in orders:
            number, order_number, price, delivery_time = order
            sql = ('UPDATE orders '
                   'SET number = %(number)s, price = %(price)s, price_rub = %(price)s * usd_exchange_rate, '
                   'delivery_time = %(delivery_time)s '
                   'WHERE order_num = %(order_num)s'
                   )
            values = {
                'number': number,
                'order_num': order_number,
                'price': price,
                'delivery_time': delivery_time
            }

            cursor.execute(sql, values)


def get_orders(order_nums: Iterable[int]) -> Iterable:
    with get_cursor(DB_NAME) as cursor:
        for order_num in order_nums:
            sql = ("SELECT number, order_num, price, to_char(delivery_time, 'DD.MM.YYYY') "
                   "FROM orders "
                   "WHERE order_num = %(order_num)s"
                   )
            values = {
                'order_num': order_num
            }
            cursor.execute(sql, values)
            yield cursor.fetchone()


def get_all_order_nums() -> List[tuple]:
    sql = ('SELECT order_num '
           'FROM orders ')

    with get_cursor(DB_NAME) as cursor:
        cursor.execute(sql)
        return cursor.fetchall()


def delete_orders(order_nums: List[int]):
    if not order_nums:
        return None
    with get_cursor(DB_NAME) as cursor:
        for order_num in order_nums:
            sql = ('DELETE FROM orders '
                   'WHERE order_num = %(order_num)s')
            values = {
                'order_num': order_num
            }
            cursor.execute(sql, values)


def delete_all_orders():
    sql = ('DELETE FROM orders')

    with get_cursor(DB_NAME) as cursor:
        cursor.execute(sql)


def order_delivery_completed(order_number: int):
    sql = ('UPDATE orders '
           'SET delivery_completed = true'
           'WHERE order_num = %(order_num)s'
           )
    values = {
        'order_num': order_number
    }

    with get_cursor(DB_NAME) as cursor:
        cursor.execute(sql, values)


def add_telegram_user(telegram_id: int):
    sql = ('INSERT INTO telegram_users'
           '    (telegram_id) '
           'VALUES '
           '    %(telegram_id)s'
           )
    values = {
        'telegram_id': telegram_id
    }

    with get_cursor(DB_NAME) as cursor:
        cursor.execute(sql, values)


def telegram_user_exist(telegram_id: int) -> bool:
    sql = ('SELECT *'
           'FROM telegram_users'
           'WHERE telegram_id = %(telegram_id)s'
           )
    values = {
        'telegram_id': telegram_id
    }

    with get_cursor(DB_NAME) as cursor:
        cursor.execute(sql, values)
        return bool(cursor.fetchone())
