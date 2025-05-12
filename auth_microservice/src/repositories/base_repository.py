# External Library imports
from pymongo.collection import Collection

# Internal library imports
from src.database_management import Database


class BaseRepository:
    def __init__(self, database: Database):
        if not isinstance(database, Database):
            raise TypeError(f"database must be of type Database, "
                            f"not {type(database).__name__}.")
        self.database = database


    def get_employees_collection(self) -> Collection:
        return self.database.get_collection("employees")
