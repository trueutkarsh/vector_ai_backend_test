"""
Storage interface later is interface betwwen main client and db

"""

from databasestorage import DatabaseStorage
from validator import Validator

class StorageInterface(object):

    def __init__(self,config):
        self._db = DatabaseStorage(config["database"])
        self._validator = Validator(self._db)

    def add_continent(self, name, population, area):
        """
        Validations to perform
            - check name is valid
        Insert into db
        Update the cache
        """
        # check name
        if not self._validate_name(name):
            return False
        # check db operation
        if not self._db.add_continent(name, population, area):
            return False

        self._validator.update_cache("population", name, population)
        self._validator.update_cache("area", name, area)
        
        return True
    
    def add_country(self, name, population, area, num_hospitals, num_rivers, num_schools, parent_continent):
        """
        Validation
            - check name is valid
            - validate area, population
        Insert into db
        Update the cache
        """
        # Check name
        if not self._validate_name(name):
            return False
        
        # check area and population
        validation_config = {
            "area": [
                {
                    "value": area,
                    "parent": parent_continent
                }
            ],
            "population": [
                {
                    "value": population,
                    "parent": parent_continent
                }
            ],
        }
        if not self._validate_values(validation_config):
            return False
        if not(
            self._db.add_country(name, population, area, num_hospitals, num_rivers, num_schools) 
            and 
            self._db.add_country_continent_relation(name, parent_continent)
        ):
            return False
        
        # Update cache
        self._validator.update_cache("population", name, population)
        self._validator.update_cache("area", name, area)
        self._validator.update_cache("num_schools", name, num_schools)

        return True

    def add_city(self, name, population, area, num_roads, num_trees, num_shops, num_schools, parent_country):
        """
        Validation
             - checkname
             - validate area, population, num_schools
        Insert into db
        Update the cache
        """
        # Check name
        if not self._validate_name(name):
            return False
        
        # check area and population
        validation_config = {
            "area": [
                {
                    "value": area,
                    "parent": parent_country
                }
            ],
            "population": [
                {
                    "value": population,
                    "parent": parent_country
                }
            ],
        }
        if not self._validate_values(validation_config):
            return False

        if not (
            self._db.add_city(name, population, area, num_roads, num_trees, num_shops, num_schools)
            and
            self._db.add_city_country_relation(name, parent_country)
        ):
            return False

        # Update cache
        self._validator.update_cache("population", name, population, True)
        self._validator.update_cache("area", name, area, True)
        self._validator.update_cache("num_schools", name, num_schools, True)

        return True

    def _validate_name(self, name):
        return self._validator.validate_name()
    
    def _validate_value(self, field_name, value, parent_name):
        return getattr(self._validator, f"validate_{field_name}")(value, parent_name)
    
    def _validate_values(self, validation_config):
        """
        validation_config = {
            "area": [
                {
                    "value": val,
                    "parent": parent
                }
            ]
            "population": [
                {
                    "value": val,
                    "parent": parent
                }
            ]
        }
        """
        for field, value_items in validation_config.iteritems():
            for item in value_items:
                if not self._validate_value(field, item["value"], item["parent"]):
                    return False
        return True