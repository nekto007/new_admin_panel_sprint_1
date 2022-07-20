from dataclasses import (
    astuple,
    fields,
)
from logging import getLogger

import psycopg2
from psycopg2.extras import execute_values


class PostgresSaver:
    def __init__(self, pg_conn: psycopg2.extensions.connection):
        self._connection = pg_conn
        self._cursor = self._connection.cursor()
        self._logger = getLogger()

    def save_all_data(self, talbe_name, data, dataclass):
        """Метод сохранения данных в таблицу PostgreSQL"""
        try:
            keys = ", ".join(field.name for field in fields(dataclass))
            execute_values(
                self._cursor,
                f"""INSERT INTO content.{talbe_name} ({keys})
                VALUES %s ON CONFLICT (id) DO NOTHING;""",
                [astuple(row) for row in data])
        except Exception as exception:
            self._logger.error(exception)
