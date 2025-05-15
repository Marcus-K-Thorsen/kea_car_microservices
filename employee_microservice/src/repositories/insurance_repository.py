# External Library imports
from typing import Optional, List

# Internal library imports
from src.entities import InsuranceEntity
from src.resources import InsuranceCreateResource, InsuranceUpdateResource
from src.repositories.base_repository import BaseRepository


class InsuranceRepository(BaseRepository):
    def get_all(self, limit: Optional[int] = None) -> List[InsuranceEntity]:
        """
        Retrieves all insurances from the Employee MySQL database.
        
        :param limit: The maximum number of insurances to retrieve (optional).
        :type limit: int | None
        :return: A list of InsuranceEntity objects.
        :rtype: list[InsuranceEntity]
        """
        insurances_query = self.session.query(InsuranceEntity)
        
        if self.limit_is_valid(limit):
            insurances_query = insurances_query.limit(limit)
        
        return insurances_query.all()
    
    def get_by_id(self, insurance_id: str) -> Optional[InsuranceEntity]:
        """
        Retrieves an insurance by ID from the Employee MySQL database.
        
        :param insurance_id: The ID of the insurance to retrieve.
        :type insurance_id: str
        :return: The insurance if found, None otherwise.
        :rtype: InsuranceEntity | None
        """
        return self.session.get(InsuranceEntity, insurance_id)
    
    def create(self, insurance_create_data: InsuranceCreateResource) -> InsuranceEntity:
        """
        Creates a new insurance in the Employee MySQL database.
        
        :param insurance_create_data: The data for the insurance to create.
        :type insurance_create_data: InsuranceCreateResource
        :return: The created insurance entity.
        :rtype: InsuranceEntity
        """
        insurance = InsuranceEntity(
            id=insurance_create_data.id,
            name=insurance_create_data.name,
            price=insurance_create_data.price
        )
        self.session.add(insurance)
        self.flush()
        self.session.refresh(insurance)
        return insurance
    
    def update(self, insurance_id: str, insurance_update_data: InsuranceUpdateResource) -> Optional[InsuranceEntity]:
        """
        Updates an existing insurance in the Employee MySQL database.
        
        :param insurance_id: The ID of the insurance to update.
        :type insurance_id: str
        :param insurance_update_data: The data to update the insurance with.
        :type insurance_update_data: InsuranceUpdateResource
        :return: The updated insurance entity if found, None otherwise.
        :rtype: InsuranceEntity | None
        """
        insurance = self.get_by_id(insurance_id)
        
        if insurance is None:
            return None
        
        for key, value in insurance_update_data.get_updated_fields().items():
            setattr(insurance, key, value)
        
        self.session.commit()
        self.session.refresh(insurance)
        
        return insurance
    
    
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
        insurance_query = self.session.query(InsuranceEntity).filter_by(name=insurance_name)
        if insurance_id is not None and isinstance(insurance_id, str):
            insurance_query = insurance_query.filter(InsuranceEntity.id != insurance_id)
        return insurance_query.first()