import os
import sqlite3
from logging import getLogger

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from models_dataclass import (
    Filmwork,
    Genre,
    GenreFilmwork,
    Person,
    PersonFilmwork,
)
from postgres_saver import PostgresSaver
from sqlite_loader import SQLiteLoader


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection, logger):
    """Основной метод загрузки данных из SQLite в Postgres"""
    try:
        postgres_saver = PostgresSaver(pg_conn)
        sqlite_loader = SQLiteLoader(connection)
        data = {
            'film_work': Filmwork,
            'genre': Genre,
            'person': Person,
            'genre_film_work': GenreFilmwork,
            'person_film_work': PersonFilmwork,
        }
        for key, value in data.items():
            import_data = sqlite_loader.format_dataclass_data(key, value)
            postgres_saver.save_all_data(key, import_data, value)
    except Exception as exception:
        logger.error(exception)


if __name__ == '__main__':
    load_dotenv()
    logger = getLogger()
    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': os.environ.get('DB_PORT', 5432)
    }
    sqlite_path = os.environ.get('SQLITE_PATH')
    with sqlite3.connect(sqlite_path) as sqlite_conn, \
            psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn, logger)
    sqlite_conn.close()
    pg_conn.close()
