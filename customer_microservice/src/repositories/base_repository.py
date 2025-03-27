# External Library imports
from typing import Optional
from pymongo.database import Database
from pymongo.collection import Collection



class BaseRepository():
    def __init__(self, database: Database):
        if not isinstance(database, Database):
            raise TypeError(f"database must be of type Database, "
                            f"not {type(database).__name__}.")
        self.database = database
    
    def limit_is_valid(self, limit: Optional[int]) -> bool:
        if limit is not None and not isinstance(limit, bool) and isinstance(limit, int) and limit > 0:
            return True
        return False
    
    def get_models_collection(self) -> Collection:
        return self.database.get_collection("models")
    
    def get_brands_collection(self) -> Collection:
        return self.database.get_collection("brands")
    
    def get_colors_collection(self) -> Collection:
        return self.database.get_collection("colors")
    
    def get_accessories_collection(self) -> Collection:
        return self.database.get_collection("accessories")
    
    def get_insurances_collection(self) -> Collection:
        return self.database.get_collection("insurances")
    
    
