import datetime
import os
import sqlite3

import psycopg2
import pytest
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

import models_dataclass

load_dotenv()

dsl = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'port': os.environ.get('DB_PORT', 5432)
}


class TestDataSQL:

    @pytest.fixture
    def connect(self):
        with sqlite3.connect(os.environ.get('SQLITE_PATH')) as sqlite_conn, \
                psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
            yield sqlite_conn, pg_conn

    def test_assert_film_work(self, connect):
        """Тест проверяющий наличие фильма из SQLite в PostgreSQl"""
        connection, pg_conn = connect
        cursor = pg_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        row_sqlite = models_dataclass.Filmwork(
            id='5e5fd2e0-be06-4806-b3ac-e8d0be6716c1',
            title='Son of the Morning Star',
            description='The life of George Armstrong Custer comes alive in this made for television movie.',
            rating=7.5,
            type='movie',
            creation_date=None,
            created=datetime.datetime(
                2021, 6, 16, 20, 14, 9, 229768,
                tzinfo=datetime.timezone.utc
            ),
            modified=datetime.datetime(
                2021, 6, 16, 20, 14, 9, 229784,
                tzinfo=datetime.timezone.utc
            ),
        )
        cursor.execute(f"SELECT * FROM content.film_work WHERE film_work.id = '{row_sqlite.id}'")
        data = cursor.fetchone()
        row_postgres_data = models_dataclass.Filmwork(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            rating=data['rating'],
            type=data['type'],
            creation_date=data['creation_date'],
            created=data['created'],
            modified=data['modified']
        )
        assert row_sqlite == row_postgres_data

    def test_assert_genre(self, connect):
        """Тест проверяющий наличие жанра из SQLite в PostgreSQl"""
        connection, pg_conn = connect
        cursor = pg_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        row_sqlite = models_dataclass.Genre(
            id='f39d7b6d-aef2-40b1-aaf0-cf05e7048011',
            name='Horror',
            description=None,
            created=datetime.datetime(
                2021, 6, 16, 20, 14, 9, 310814,
                tzinfo=datetime.timezone.utc
            ),
            modified=datetime.datetime(
                2021, 6, 16, 20, 14, 9, 310830,
                tzinfo=datetime.timezone.utc
            ),
        )
        cursor.execute(f"SELECT * FROM content.genre WHERE genre.id = '{row_sqlite.id}'")
        data = cursor.fetchone()
        row_postgres_data = models_dataclass.Genre(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            created=data['created'],
            modified=data['modified'],
        )
        assert row_sqlite == row_postgres_data

    def test_assert_person(self, connect):
        """Тест проверяющий наличие актера из SQLite в PostgreSQl"""
        connection, pg_conn = connect
        cursor = pg_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        row_sqlite = models_dataclass.Person(
            id='618ed131-f181-4932-b3cb-e637a87d594e',
            full_name='Jerry Siegel',
            created=datetime.datetime(
                2021, 6, 16, 20, 14, 9, 323107,
                tzinfo=datetime.timezone.utc
            ),
            modified=datetime.datetime(
                2021, 6, 16, 20, 14, 9, 323127,
                tzinfo=datetime.timezone.utc
            )
        )
        cursor.execute(f"SELECT * FROM content.person WHERE person.id = '{row_sqlite.id}'")
        data = cursor.fetchone()
        row_postgres_data = models_dataclass.Person(
            full_name=data['full_name'],
            created=data['created'],
            modified=data['modified'],
            id=data['id']
        )
        assert row_sqlite == row_postgres_data

    def test_assert_genre_film_work(self, connect):
        """Тест проверяющий наличие промежуточных данных
        из SQLite в PostgreSQl"""
        connection, pg_conn = connect
        cursor = pg_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        row_sqlite = models_dataclass.GenreFilmwork(
            id='ed9f656c-43d7-47fc-b66b-8f477da7431c',
            film_work_id='5f5ac9fd-dedd-46f1-8bfa-cf6f76853f50',
            genre_id='3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
            created=datetime.datetime(
                2021, 6, 16, 20, 14, 9, 580594,
                tzinfo=datetime.timezone.utc
            )
        )
        cursor.execute(f"SELECT * FROM content.genre_film_work WHERE genre_film_work.id = '{row_sqlite.id}'")
        data = cursor.fetchone()
        row_postgres_data = models_dataclass.GenreFilmwork(
            created=data['created'],
            film_work_id=data['film_work_id'],
            genre_id=data['genre_id'],
            id=data['id'],

        )
        assert row_sqlite == row_postgres_data

    def test_assert_person_film_work(self, connect):
        """A test that verifies the presence of intermediate data from SQLite to PostgreSQL"""
        connection, pg_conn = connect
        cursor = pg_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        row_sqlite = models_dataclass.PersonFilmwork(
            id='99643bd6-87a7-4184-828d-b64b52426694',
            film_work_id='eed327be-1d0d-4adf-8391-8c8491747f59',
            person_id='165bde3f-82fd-4863-a600-75e350b35914',
            role='actor',
            created=datetime.datetime(
                2021, 6, 16, 20, 14, 9, 712243,
                tzinfo=datetime.timezone.utc
            ),
        )
        cursor.execute(f"SELECT * FROM content.person_film_work WHERE person_film_work.id = '{row_sqlite.id}'")
        data = cursor.fetchone()
        row_postgres_data = models_dataclass.PersonFilmwork(
            created=data['created'],
            film_work_id=data['film_work_id'],
            person_id=data['person_id'],
            id=data['id'],
            role=data['role']

        )
        assert row_sqlite == row_postgres_data

    def test_number_records(self, connect):
        """A test that checks the number of SQLite and PostgreSQL records"""
        connection, pg_conn = connect
        sqlite_cursor = connection.cursor()
        pg_cursor = pg_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sqlite_cursor.execute(
            "SELECT count(*) FROM film_work"
        )
        pg_cursor.execute(
            "SELECT count(*) FROM content.film_work"
        )
        assert sqlite_cursor.fetchone()[0] == pg_cursor.fetchone()[0]
        sqlite_cursor.execute(
            "SELECT count(*) FROM genre"
        )
        pg_cursor.execute(
            "SELECT count(*) FROM content.genre"
        )
        assert sqlite_cursor.fetchone()[0] == pg_cursor.fetchone()[0]
        sqlite_cursor.execute(
            "SELECT count(*) FROM person"
        )
        pg_cursor.execute(
            "SELECT count(*) FROM content.person"
        )
        assert sqlite_cursor.fetchone()[0] == pg_cursor.fetchone()[0]
        sqlite_cursor.execute(
            "SELECT count(*) FROM genre_film_work"
        )
        pg_cursor.execute(
            "SELECT count(*) FROM content.genre_film_work"
        )
        assert sqlite_cursor.fetchone()[0] == pg_cursor.fetchone()[0]
        sqlite_cursor.execute(
            "SELECT count(*) FROM person_film_work"
        )
        pg_cursor.execute(
            "SELECT count(*) FROM content.person_film_work"
        )
        assert sqlite_cursor.fetchone()[0] == pg_cursor.fetchone()[0]
