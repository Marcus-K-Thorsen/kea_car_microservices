# External Library imports
from typing import Optional, List, Dict, Any
from pymongo.cursor import Cursor

# Internal library imports
from src.entities import InsuranceEntity
from src.repositories.base_repository import BaseRepository


class InsuranceRepository(BaseRepository):

    def get_all(self, limit: Optional[int] = None) -> List[InsuranceEntity]:
        insurances_collection = self.get_insurances_collection()
        insurances_query: Cursor[Dict[str, Any]] = insurances_collection.find()
        
        if self.limit_is_valid(limit):
            insurances_query = insurances_query.limit(limit)
        
        return [InsuranceEntity(**insurance) for insurance in insurances_query]


    def get_by_id(self, insurance_id: str) -> Optional[InsuranceEntity]:
        insurances_collection = self.get_insurances_collection()
        insurance_query = insurances_collection.find_one({"_id": insurance_id})
        
        if insurance_query is not None:
            return InsuranceEntity(**insurance_query)
        return None
