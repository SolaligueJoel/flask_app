DROP TABLE IF EXISTS localidad;

CREATE TABLE localidad(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [location] TEXT NOT NULL,
    [price_min] INTEGER NOT NULL,
    [price_max] INTEGER NOT NULL
);