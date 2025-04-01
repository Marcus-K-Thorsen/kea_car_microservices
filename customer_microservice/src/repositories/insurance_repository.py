"""
**Insurance Repository Module**

This module defines the `InsuranceRepository` class, which provides methods for interacting
with the MongoDB collection for insurances. It extends the `BaseRepository` class and
implements insurance-specific database operations.

Key Responsibilities:

- Retrieve all insurances with optional limits.
- Retrieve a specific insurance by its ID.
"""

# External Library imports
from typing import Optional, List, Dict, Any
from pymongo.cursor import Cursor

# Internal library imports
from src.entities import InsuranceEntity
from src.repositories.base_repository import BaseRepository


class InsuranceRepository(BaseRepository):
    """
    Repository for managing insurance-related database operations.

    This class provides methods to interact with the MongoDB collection for insurances,
    including retrieving all insurances or a specific insurance by its ID.
    """

    def get_all(self, limit: Optional[int] = None) -> List[InsuranceEntity]:
        """
        Retrieves all insurances from the database, with an optional limit.

        This method queries the MongoDB collection for insurances and returns a list
        of `InsuranceEntity` objects. If a limit is provided, the number of results
        is restricted to the specified value.

        :param limit: The maximum number of insurances to retrieve (optional).
        :type limit: int | None
        :return: A list of `InsuranceEntity` objects.
        :rtype: List[InsuranceEntity]
        """
        insurances_collection = self.get_insurances_collection()
        insurances_query: Cursor[Dict[str, Any]] = insurances_collection.find()
        
        if self.limit_is_valid(limit):
            insurances_query = insurances_query.limit(limit)
        
        return [InsuranceEntity(**insurance) for insurance in insurances_query]

    def get_by_id(self, insurance_id: str) -> Optional[InsuranceEntity]:
        """
        Retrieves a specific insurance by its ID.

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
