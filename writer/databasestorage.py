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
    def add_continent(self, name, population):
        self._cursor.execute("""
            INSERT INTO continent (name, population)
            VALUES (%s, %s)
        """, (name, population))
        if (self._cursor.count != 1):
            raise Exception(
                f"Unsuccess insert value ({name}, {population})"
            )
        
        


