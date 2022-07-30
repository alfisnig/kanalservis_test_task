from typing import List
from contextlib import  contextmanager
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import PG_USER, PG_PASSWORD, PG_HOST, PG_PORT


def get_db_connection(database_name: str = None) -> psycopg2.extensions.connection:
    try:
        connection = psycopg2.connect(user=PG_USER,
                                      password=PG_PASSWORD,
                                      host=PG_HOST,
                                      port=PG_PORT,
                                      database=database_name)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    except (Exception, Error) as error:
        print("PostgreSQL error", error)
    finally:
        return connection


@contextmanager
def get_cursor(database_name: str = None, **kwargs):
    connection = get_db_connection(database_name)
    cursor = connection.cursor(**kwargs)
    yield cursor
    cursor.close()
    connection.close()
