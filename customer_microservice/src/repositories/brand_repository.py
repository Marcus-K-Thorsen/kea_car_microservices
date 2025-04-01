"""
**Brand Repository Module**

This module defines the `BrandRepository` class, which provides methods for interacting
with the MongoDB collection for car brands. It extends the `BaseRepository` class and
implements brand-specific database operations.

Key Responsibilities:

- Retrieve all car brands with optional limits.
- Retrieve a specific car brand by its ID.
"""

# External Library imports
from typing import Optional, List, Dict, Any
from pymongo.cursor import Cursor

# Internal library imports
from src.entities import BrandEntity
from src.repositories.base_repository import BaseRepository


class BrandRepository(BaseRepository):
    """
    Repository for managing brand-related database operations.

    This class provides methods to interact with the MongoDB collection for car brands,
    including retrieving all brands or a specific car brand by its ID.
    """

    def get_all(self, limit: Optional[int] = None) -> List[BrandEntity]:
        """
        Retrieves all car brands from the database, with an optional limit.

        This method queries the MongoDB collection for car brands and returns a list
        of `BrandEntity` objects. If a limit is provided, the number of results
        is restricted to the specified value.

        :param limit: The maximum number of car brands to retrieve (optional).
        :type limit: int | None
        :return: A list of `BrandEntity` objects.
        :rtype: List[BrandEntity]
        """
        brands_collection = self.get_brands_collection()
        brands_query: Cursor[Dict[str, Any]] = brands_collection.find()
        
        if self.limit_is_valid(limit):
            brands_query = brands_query.limit(limit)
        
        return [BrandEntity(**brand) for brand in brands_query]

    def get_by_id(self, brand_id: str) -> Optional[BrandEntity]:
        """
        Retrieves a specific car brand by its ID.

        This method queries the MongoDB collection for a car brand with the given ID
        and returns it as a `BrandEntity` object. If no car brand is found, it returns `None`.

        :param brand_id: The ID of the car brand to retrieve.
        :type brand_id: str
        :return: The `BrandEntity` object if found, otherwise `None`.
        :rtype: BrandEntity | None
        """
        brands_collection = self.get_brands_collection()
        brand_query = brands_collection.find_one({"_id": brand_id})
        
        if brand_query is not None:
            return BrandEntity(**brand_query)
        
        return None
