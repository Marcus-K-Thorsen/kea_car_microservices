# External Library imports
from typing import Optional, List, Dict, Any
from pymongo.cursor import Cursor

# Internal library imports
from src.entities import AccessoryEntity
from src.repositories.base_repository import BaseRepository


class AccessoryRepository(BaseRepository):

    def get_all(self, limit: Optional[int] = None) -> List[AccessoryEntity]:
        accessories_collection = self.get_accessories_collection()
        accessories_query: Cursor[Dict[str, Any]] = accessories_collection.find()
        
        if self.limit_is_valid(limit):
            accessories_query = accessories_query.limit(limit)
        
        return [AccessoryEntity(**accessory) for accessory in accessories_query]


    def get_by_id(self, accessory_id: str) -> Optional[AccessoryEntity]:
        accessories_collection = self.get_accessories_collection()
        accessory_query = accessories_collection.find_one({"_id": accessory_id})
        
        if accessory_query is not None:
            return AccessoryEntity(**accessory_query)
        
        return None
    