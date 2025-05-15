# External Library imports
from typing import Optional, List

# Internal library imports
from src.entities import InsuranceEntity, InsuranceMessage
from src.repositories.base_repository import BaseRepository


class InsuranceRepository(BaseRepository):
    def get_by_id(self, insurance_id: str) -> Optional[InsuranceEntity]:
        """
        Retrieves a specific insurance by its ID from the Customer Mongo database.

        This method queries the MongoDB collection for an insurance with the given ID
        and returns it as an `InsuranceEntity` object. If no insurance is found, it
        returns `None`.

        :param insurance_id: The ID of the insurance to retrieve.
        :type insurance_id: str
        :return: The `InsuranceEntity` object if found, otherwise `None`.
        :rtype: InsuranceEntity | None
        """
        insurances_collection = self.get_insurances_collection()
        insurance_query = insurances_collection.find_one({"_id": insurance_id})
        
        if insurance_query is not None:
            return InsuranceEntity(**insurance_query)
        return None
    
    def create(self, insurance_create_data: InsuranceMessage) -> InsuranceEntity:
        """
        Creates a new insurance in the Customer Mongo database.
        
        :param insurance_create_data: The data for the insurance to create.
        :type insurance_create_data: InsuranceMessage
        :return: The created insurance entity.
        :rtype: InsuranceEntity
        """
        insurances_collection = self.get_insurances_collection()
        insurance_entity = InsuranceEntity(
            _id=insurance_create_data.id,
            name=insurance_create_data.name,
            price=insurance_create_data.price,
            created_at=insurance_create_data.created_at,
            updated_at=insurance_create_data.updated_at
        )
        
        insurances_collection.insert_one(insurance_entity.to_mongo_dict(exlude_id=False))
        return insurance_entity
        
    
    def update(self, insurance_update_data: InsuranceMessage) -> Optional[InsuranceEntity]:
        """
        Updates an existing insurance in the Customer Mongo database.
        
        :param insurance_update_data: The data to update the insurance with.
        :type insurance_update_data: InsuranceMessage
        :return: The updated insurance entity if found, None otherwise.
        :rtype: InsuranceEntity | None
        """
        insurances_collection = self.get_insurances_collection()
        updated_insurance = insurances_collection.find_one_and_update(
            {"_id": insurance_update_data.id},
            {"$set": insurance_update_data.to_mongo_dict(exlude_id=True)},
            return_document=True
        )
        
        if updated_insurance is not None:
            return InsuranceEntity(**updated_insurance)
        
        return None
    
    
    def get_by_name(self, insurance_name: str, insurance_id: Optional[str] = None) -> Optional[InsuranceEntity]:
        """
        Retrieves an insurance by name from the Employee MySQL database.
        
        :param insurance_name: The name of the insurance to retrieve.
        :type insurance_name: str
        :param insurance_id: The ID of the insurance to exclude from the search (optional).
        :type insurance_id: str | None
        :return: The insurance if found, None otherwise.
        :rtype: InsuranceEntity | None
        """
    
        insurance_query = {"name": insurance_name}
        if insurance_id is not None and isinstance(insurance_id, str):
            insurance_query["_id"] = {"$ne": insurance_id}
        found_insurance = self.get_insurances_collection().find_one(insurance_query)
        if found_insurance is not None:
            return InsuranceEntity(**found_insurance)
        return None