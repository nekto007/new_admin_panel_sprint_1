import sqlite3
from logging import getLogger


def reformat_fields(element):
    """A function that corrects fields in date classes to be correctly passed to PostgreSQL"""
    if "created_at" in element:
        element["created"] = element["created_at"]
        del (element["created_at"])
    if "updated_at" in element:
        element["modified"] = element["updated_at"]
        del (element["updated_at"])
    if "file_path" in element:
        del (element["file_path"])
    return element


class SQLiteLoader:
    def __init__(self, connection):
        self._connection = connection
        self._logger = getLogger()
        self.batch_size = 100

    def dict_factory(self, cursor, row):
        """Method to retrieve data in dict format from SQLite"""
        dict_sqlite = {}
        for idx, column in enumerate(cursor.description):
            dict_sqlite[column[0]] = row[idx]
        return dict_sqlite

    def get_data_sqlite(self, table: str):
        """Main method for getting data and SQLite tables"""
        try:
            self._connection.row_factory = self.dict_factory
            _curs = self._connection.cursor()
            try:
                _curs.execute(f"SELECT * FROM {table};")  # noqa: S608
            except sqlite3.Error as e:
                raise e
            while rows := _curs.fetchmany(size=self.batch_size):
                if rows:
                    yield from rows
        except Exception as exception:
            self._logger.error(exception)

    def format_dataclass_data(self, table: str, dataclass):
        """Method for pushing data into a dataclass"""
        data = self.get_data_sqlite(table)
        return [dataclass(**reformat_fields(element)) for element in data]
