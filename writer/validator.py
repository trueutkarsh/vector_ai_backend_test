"""
This module is for validating that, data passed to database layer for
DB operations

Data types in DB tables, Validation to be performed
 - string -> name - Check that name only contains alphabets
 - int -> population, num_* -> 
            e.g 
            check the consistency of the values (population)
            1. sum(population(cities)) <= population (country)
            2. sum(population(countries)) <= population (continent)
            check the consistency of the values (num_schools)
            1. sum(num_schools(cities)) <= num_schools (country)
 - double -> area
            1. sum(area(cities)) <= area (country)
            2. sum(area(countries)) <= area (continent)
    
 - Idea is to maintain an in memory cache
    - The cache warmas on start up, querying corresponding values in DB
    - For every insert operation on DB, each value will goes through a list of checks
        - Either string validation
        - Or Value validation (cache lookup)
    - If all goes well, make the db operation
        - If the operation is successfull update the cache, forward the message
        - If unsuccessful, don't update the cache, carry the error message forward, 
          catch it in service layer   

"""

class Validator(object):

    def __init__(self, db):
        self._db = db
        self._reset_cache()

    def validate_name(self, name):
        return isinstance(name, str) and name.isalpha()

    def validate_population(self, population, parent):
        return self._cache["population"].get(f"aggregate{parent}", 0) + population\
            < self._cache["population"].get(parent, 0)

    def validate_area(self, area, parent):
        return self._cache["area"].get(f"aggregate{parent}", 0.0) + area\
            < self._cache["area"].get(parent, 0.0)

    def validate_schools(self, schools, parent):
        return self._cache["schools"].get(f"aggregate{parent}", 0.0) + schools\
            < self._cache["schools"].get(parent, 0.0)

    def update_cache(self, field, name, value, is_leaf=False):
        self._cache[field][name] = value
        if not is_leaf:
            self._cache[field][f"aggreagate{name}"] = self._cache[field].get(f"aggregate{name}", 0) + value

    def _reset_cache(self):
        self._cache = {
            "population": {},
            "area": {},
            "schools": {},
        }
        self._fill_cache(self._db.get_population(), "population")
        self._fill_cache(self._db.get_population_aggregate(), "population", "aggregate")
        self._fill_cache(self._db.get_area(), "area")
        self._fill_cache(self._db.get_area_aggregate(), "area", "aggregate")
        self._fill_cache(self._db.get_num_schools(), "schools")
        self._fill_cache(self._db.get_num_schools_aggregate(), "schools", "aggregate")
    
    def _fill_cache(self, rows, key, prefix=""):
        for row in rows:
            self._cache[key][prefix+row[0]] = row[1]

