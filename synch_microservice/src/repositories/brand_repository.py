# External Library imports
from typing import Optional

# Internal library imports
from src.entities import BrandEntity
from src.repositories.base_repository import BaseRepository


class BrandRepository(BaseRepository):
    def get_by_id(self, brand_id: str) -> Optional[BrandEntity]:
        """
        Retrieves a specific brand by its ID from the Customer Mongo database.

        This method queries the MongoDB collection for a brand with the given ID
        and returns it as an `BrandEntity` object. If no brand is found, it
        returns `None`.

        :param brand_id: The ID of the brand to retrieve.
        :type brand_id: str
        :return: The `BrandEntity` object if found, otherwise `None`.
        :rtype: BrandEntity | None
        """
        brands_collection = self.get_brands_collection()
        brand_query = brands_collection.find_one({"_id": brand_id})
        
        if brand_query is not None:
            return BrandEntity(**brand_query)
        return None
