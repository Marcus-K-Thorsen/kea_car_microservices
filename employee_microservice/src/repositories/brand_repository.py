# External Library imports
from typing import Optional, List

# Internal library imports
from src.entities import BrandEntity
from src.repositories.base_repository import BaseRepository

class BrandRepository(BaseRepository):
    def get_all(self, limit: Optional[int] = None) -> List[BrandEntity]:
        """
        Retrieves all brands from the Employee MySQL database.
        
        :param limit: The maximum number of brands to retrieve (optional).
        :type limit: int | None
        :return: A list of BrandEntity objects.
        :rtype: list[BrandEntity]
        """
        brands_query = self.session.query(BrandEntity)

        if self.limit_is_valid(limit):
            brands_query = brands_query.limit(limit)

        return brands_query.all()


    def get_by_id(self, brand_id: str) -> Optional[BrandEntity]:
        """
        Retrieves a brand by ID from the Employee MySQL database.
        
        :param brand_id: The ID of the brand to retrieve.
        :type brand_id: str
        :return: A BrandEntity object if found, None otherwise.
        :rtype: BrandEntity | None
        """
        return self.session.get(BrandEntity, brand_id)
    