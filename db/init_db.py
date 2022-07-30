import psycopg2
from connection import get_cursor
from config import DB_NAME


def create_db():
    sql = f'CREATE database {DB_NAME}'
    try:
        with get_cursor() as cursor:
            cursor.execute(sql)
    except psycopg2.errors.DuplicateDatabase:
        print("manga_db already exist.")


def create_orders_table():
    sql = ('CREATE TABLE IF NOT EXISTS orders ('
           '    id SERIAL PRIMARY KEY,'
           '    number integer NOT NULL,'
           '    order_num integer NOT NULL,'
           '    price real NOT NULL,'
           '    price_rub real NOT NULL,'
           '    delivery_time DATE NOT NULL,'
           '    delivery_completed boolean NOT NULL DEFAULT FALSE,'
           '    creation_date DATE NOT NULL DEFAULT current_date,'
           '    UNIQUE(order_num)'
           ')')

    with get_cursor(DB_NAME) as cursor:
        cursor.execute(sql)


def create_telegram_users_table():
    sql = ('CREATE TABLE IF NOT EXISTS telegram_users ('
           '    id SERIAL PRIMARY KEY,'
           '    telegram_id integer NOT NULL,'
           '    UNIQUE(telegram_id)'
           ')')

    with get_cursor(DB_NAME) as cursor:
        cursor.execute(sql)


if __name__ == '__main__':
    print('Creating database...')
    create_db()
    print('Creating orders table...')
    create_orders_table()
    print('Creating telegram users table...')
    create_telegram_users_table()
    print('Success!')
