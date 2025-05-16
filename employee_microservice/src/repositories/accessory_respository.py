# External Library imports
from typing import Optional, List

# Internal library imports
from src.entities import AccessoryEntity
from src.repositories.base_repository import BaseRepository



class AccessoryRepository(BaseRepository):
    
    def get_all(self, limit: Optional[int] = None) -> List[AccessoryEntity]:
        """
        Retrieves all accessories from the Employee MySQL database.
        
        :param limit: The maximum number of accessories to retrieve (optional).
        :type limit: int | None
        :return: A list of AccessoryEntity objects.
        :rtype: list[AccessoryEntity]
        """
        accessories_query = self.session.query(AccessoryEntity)
        if self.limit_is_valid(limit):
            accessories_query = accessories_query.limit(limit)
        return accessories_query.all()


    def get_by_id(self, accessory_id: str) -> Optional[AccessoryEntity]:
        """
        Retrieves an accessory by ID from the Employee MySQL database.
        
        :param accessory_id: The ID of the accessory to retrieve.
        :type accessory_id: str
        :return: The accessory if found, None otherwise.
        :rtype: AccessoryEntity | None
        """
        return self.session.get(AccessoryEntity, accessory_id)


