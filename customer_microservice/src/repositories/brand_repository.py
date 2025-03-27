# External Library imports
from typing import Optional, List, Dict, Any
from pymongo.cursor import Cursor

# Internal library imports
from src.entities import BrandEntity
from src.repositories.base_repository import BaseRepository


class BrandRepository(BaseRepository):

    def get_all(self, limit: Optional[int] = None) -> List[BrandEntity]:
        brands_collection = self.get_brands_collection()
        brands_query: Cursor[Dict[str, Any]] = brands_collection.find()
        
        if self.limit_is_valid(limit):
            brands_query = brands_query.limit(limit)
        
        return [BrandEntity(**brand) for brand in brands_query]

    def get_by_id(self, brand_id: str) -> Optional[BrandEntity]:
        brands_collection = self.get_brands_collection()
        brand_query = brands_collection.find_one({"_id": brand_id})
        
        if brand_query is not None:
            return BrandEntity(**brand_query)
        
        return None