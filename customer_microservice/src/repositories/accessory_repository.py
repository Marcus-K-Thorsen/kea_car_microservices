"""
**Accessory Repository Module**

This module defines the `AccessoryRepository` class, which provides methods for interacting
with the MongoDB collection for accessories. It extends the `BaseRepository` class and
implements accessory-specific database operations.

Key Responsibilities:

- Retrieve all accessories with optional limits.
- Retrieve a specific accessory by its ID.
"""

# External Library imports
from typing import Optional, List, Dict, Any
from pymongo.cursor import Cursor

# Internal library imports
from src.entities import AccessoryEntity
from src.repositories.base_repository import BaseRepository


class AccessoryRepository(BaseRepository):
    """
    Repository for managing accessory-related database operations.

    This class provides methods to interact with the MongoDB collection for accessories,
    including retrieving all accessories or a specific accessory by its ID.
    """

    def get_all(self, limit: Optional[int] = None) -> List[AccessoryEntity]:
        """
        Retrieves all accessories from the database, with an optional limit.

        This method queries the MongoDB collection for accessories and returns a list
        of `AccessoryEntity` objects. If a limit is provided, the number of results
        is restricted to the specified value.

        :param limit: The maximum number of accessories to retrieve (optional).
        :type limit: int | None
        :return: A list of `AccessoryEntity` objects.
        :rtype: List[AccessoryEntity]
        """
        accessories_collection = self.get_accessories_collection()
        accessories_query: Cursor[Dict[str, Any]] = accessories_collection.find()
        
        if self.limit_is_valid(limit):
            accessories_query = accessories_query.limit(limit)
        
        return [AccessoryEntity(**accessory) for accessory in accessories_query]


    def get_by_id(self, accessory_id: str) -> Optional[AccessoryEntity]:
        """
        Retrieves a specific accessory by its ID.

        This method queries the MongoDB collection for an accessory with the given ID
        and returns it as an `AccessoryEntity` object. If no accessory is found, it
        returns `None`.

        :param accessory_id: The ID of the accessory to retrieve.
        :type accessory_id: str
        :return: The `AccessoryEntity` object if found, otherwise `None`.
        :rtype: AccessoryEntity | None
        """
        accessories_collection = self.get_accessories_collection()
        accessory_query = accessories_collection.find_one({"_id": accessory_id})
        
        if accessory_query is not None:
            return AccessoryEntity(**accessory_query)
        
        return None
