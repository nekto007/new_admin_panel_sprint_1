CREATE SCHEMA IF NOT EXISTS content;

-- #Создаем таблицу content.film_work
CREATE TABLE IF NOT EXISTS content.film_work
(
    id            uuid PRIMARY KEY,
    title         TEXT NOT NULL,
    description   TEXT,
    creation_date DATE,
    rating        FLOAT,
    type          TEXT NOT NULL,
    created       timestamp with time zone,
    modified      timestamp with time zone
);

-- #Создаем таблицу content.genre
CREATE TABLE IF NOT EXISTS content.genre
(
    id          uuid PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT,
    created     timestamp with time zone,
    modified    timestamp with time zone
);

-- #Создаем таблицу content.genre_film_work
CREATE TABLE IF NOT EXISTS content.genre_film_work
(
    id           uuid PRIMARY KEY,
    genre_id     uuid NOT NULL REFERENCES content.genre (id) ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
    created      timestamp with time zone
);

-- #Создаем таблицу content.person
CREATE TABLE IF NOT EXISTS content.person
(
    id        uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created   timestamp with time zone,
    modified  timestamp with time zone
);

-- #Создаем таблицу content.person_film_work
CREATE TABLE IF NOT EXISTS content.person_film_work
(
    id           uuid PRIMARY KEY,
    film_work_id uuid NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
    person_id    uuid NOT NULL REFERENCES content.person (id) ON DELETE CASCADE,
    role         TEXT NOT NULL,
    created      timestamp with time zone
);

-- #Создаем индекс для таблицы content.film_work с полями (creation_date, rating)
CREATE INDEX film_work_creation_date_idx ON content.film_work (creation_date, rating);

-- #Создаем уникальный индекс для таблицы content.person_film_work с полями (film_work_id, person_id, role)
CREATE UNIQUE INDEX film_work_person_role_idx ON content.person_film_work (film_work_id, person_id, role);

-- #Создаем индекс для таблицы content.genre_film_work с полями (genre_id, film_work_id)
CREATE UNIQUE INDEX genre_film_work_idx ON content.genre_film_work (genre_id, film_work_id);