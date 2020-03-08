"""
This module will interact with Database
Service layer will be build on top of this
"""
"""
Create DatabaseStorage class
 -init (config)
 -get_handle/get_connection
    -functions to read/write to DB
 -Database Access Tutorial[https://pynative.com/python-postgresql-tutorial/]
"""
import psycopg2
from psycopg2 import Error


def catch_error(func):
    def _wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            return True
        except (Exception, Error) as error:
            # TODO: Log here
            print(f"Unsuccessfull opertion {error}")
            return False

    return _wrapper


class DatabaseStorage(object):
    def __init__(self, config):
        self._db_config = config
        self._cursor = self._get_cursor()

    def __del__(self):
        self._conn.close()

    def _get_cursor(self):
        self._conn = psycopg2.connect(**self._db_config)
        self._conn.autocommit = True
        return self._conn.cursor()

    def close(self):
        self._cursor.close()
        self._conn.close()

    @catch_error
    def test_get_all_tables(self):
        self._cursor.execute(
            """
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'
            """
        )
        for table in self._cursor.fetchall():
            self._cursor.execute(f"select * from {table[0]}")
            print(table[0], self._cursor.fetchall())

    @catch_error
    def add_continent(self, name, population, area):
        self._cursor.execute(
            """
            INSERT INTO continent (name, population, area)
            VALUES (%s, %s, %s)
        """,
            (name, population, area),
        )
        if self._cursor.rowcount != 1:
            raise Exception(f"Unsuccessful insert values ({name}, {population}, {area})")
    
    @catch_error
    def add_country(self, name, population, area, num_hospitals, num_rivers, num_schools):
        self._cursor.execute(
            """
            INSERT INTO country (name, population, area, num_hospitals, num_rivers, num_schools)
            VALUES
            (%s, %s, %s, %s, %s, %s)
            """,
            (name, population, area, num_hospitals, num_rivers, num_schools),
        )
        if self._cursor.rowcount != 1:
            raise Exception(
                f"""
                Unsuccessful insert values 
                ({name}, {population}, {num_hospitals}, {num_rivers}, {num_schools}) 
                """
            )
    @catch_error
    def add_city(self, name, population, area, num_roads, num_trees, num_shops, num_schools):
        self._cursor.execute(
            """
            INSERT INTO city (name, population, area, num_roads, num_trees, num_shops, num_schools)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s)
            """,
            (name, population, area, num_roads, num_trees, num_shops, num_schools),
        )
        if self._cursor.rowcount != 1:
            raise Exception(
                f"""
                Unsuccessful insert values 
                ({name}, {population}, {area}, {num_roads}, {num_trees}, {num_shops}, {num_schools}) 
                """
            )
    
    @catch_error
    def add_city_country_relation(self, city_name, country_name):

        self._cursor.execute(
            """
            INSERT INTO city_country (city_name, country_name)
            VALUES
            (%s, %s)
            """,
            (city_name, country_name)
        )
        if self._cursor.rowcount != 1:
            raise Exception(
                f"""
                Unsuccessful insert values ({city_name}, {country_name}) 
                """
            )

    @catch_error
    def add_country_continent_relation(self, country_name, continent_name):

        self._cursor.execute(
            """
            INSERT INTO country_continent (country_name, continent_name)
            VALUES
            (%s, %s)
            """,
            (country_name, continent_name)
        )
        if self._cursor.rowcount != 1:
            raise Exception(
                f"""
                Unsuccessful insert values ({country_name}, {continent_name}) 
                """
            )
    
    def get_population(self):
        """
        Get all population data for country and continent
        """
        self._cursor.execute(
            """
            SELECT name, population FROM continent
            UNION
            SELECT name, population FROM country
            """
        )
        return self._cursor.fetchall()

    def get_area(self):
        """
        Get all area data for country and continent
        """
        self._cursor.execute(
            """
            SELECT name, area FROM continent
            UNION
            SELECT name, area FROM country
            """
        )
        return self._cursor.fetchall()
        
    def get_num_schools(self):
        """
        Get all num_schools data for country and continent
        """
        self._cursor.execute(
            """
            SELECT name, num_schools FROM country
            """
        )
        return self._cursor.fetchall()
        

    def get_population_aggregate(self):
        """
        Get all population aggregate for city and country 
        w.r.t to country and and continent repectively
        """

        self._cursor.execute(
            """
            SELECT country_name, sum(population)
            FROM
            city C JOIN city_country CC 
            ON
            C.name = CC.city_name
            GROUP BY
            country_name
            UNION
            SELECT continent_name, sum(population)
            FROM
            country C JOIN country_continent CC 
            ON
            C.name = CC.country_name
            GROUP BY
            continent_name
            """
        )
        return self._cursor.fetchall()

    def get_area_aggregate(self):
        """
        Get all area aggregate for city and country 
        w.r.t to country and and continent repectively
        """

        self._cursor.execute(
            """
            SELECT country_name, sum(area)
            FROM
            city C JOIN city_country CC 
            ON
            C.name = CC.city_name
            GROUP BY
            country_name
            UNION
            SELECT continent_name, sum(area)
            FROM
            country C JOIN country_continent CC 
            ON
            C.name = CC.country_name
            GROUP BY
            continent_name
            """
        )
        return self._cursor.fetchall()

    def get_num_schools_aggregate(self):
        """
        Get all num_schools aggregate for city and country 
        w.r.t to country and and continent repectively
        """

        self._cursor.execute(
            """
            SELECT country_name, sum(num_schools)
            FROM
            city C JOIN city_country CC 
            ON
            C.name = CC.city_name
            GROUP BY
            country_name
            """
        )
        return self._cursor.fetchall()
