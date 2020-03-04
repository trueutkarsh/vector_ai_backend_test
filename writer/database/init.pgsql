
CREATE TABLE IF NOT EXISTS continent(
    name varchar(30) PRIMARY KEY,
    population BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS country(
    name varchar(30) PRIMARY KEY,
    population BIGINT NOT NULL,
    num_hospitals INTEGER NOT NULL,
    num_rivers INTEGER NOT NULL,
    num_schools INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS city(
    name varchar(30) PRIMARY KEY,
    area decimal NOT NULL,
    num_roads INTEGER NOT NULL,
    num_trees INTEGER NOT NULL,
    num_shops INTEGER NOT NULL,
    num_schools INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS city_country(
    city_name varchar(30),
    country_name varchar(30),
    FOREIGN KEY (city_name) REFERENCES city(name),
    FOREIGN KEY (country_name) REFERENCES country(name)
);

CREATE TABLE IF NOT EXISTS country_continent(
    country_name varchar(30),
    continent_name varchar(30),
    FOREIGN KEY (country_name) REFERENCES country(name),
    FOREIGN KEY (continent_name) REFERENCES continent(name)
);
