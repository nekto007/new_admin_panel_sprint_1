import uuid
from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class Filmwork:
    id: uuid.UUID
    title: str
    description: str
    creation_date: date
    rating: float
    type: str
    created: datetime
    modified: datetime


@dataclass(frozen=True)
class Genre:
    id: uuid.UUID
    name: str
    description: str
    created: datetime
    modified: datetime


@dataclass(frozen=True)
class Person:
    id: uuid.UUID
    full_name: str
    created: datetime
    modified: datetime


@dataclass(frozen=True)
class GenreFilmwork:
    id: uuid.UUID
    genre_id: uuid.UUID
    film_work_id: uuid.UUID
    created: datetime


@dataclass(frozen=True)
class PersonFilmwork:
    id: uuid.UUID
    person_id: uuid.UUID
    film_work_id: uuid.UUID
    role: str
    created: datetime
