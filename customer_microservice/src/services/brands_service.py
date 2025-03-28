# External Library imports
from typing import List, Optional

# Internal library imports
from src.database_management import Database
from src.repositories import BrandRepository
from src.resources import BrandReturnResource
from src.exceptions import UnableToFindIdError


def get_all(
        database: Database,
        brands_limit: Optional[int] = None
) -> List[BrandReturnResource]:
    
    repository = BrandRepository(database)
    
    if isinstance(brands_limit, bool) or not (isinstance(brands_limit, int) or brands_limit is None):
        raise TypeError(f"brands_limit must be of type int or None, "
                        f"not {type(brands_limit).__name__}.")

    brands = repository.get_all(limit=brands_limit)
    
    return [brand.as_resource() for brand in brands]


def get_by_id(
        database: Database,
        brand_id: str
) -> BrandReturnResource:
    
    repository = BrandRepository(database)
    
    if not isinstance(brand_id, str):
        raise TypeError(f"brand_id must be of type str, "
                        f"not {type(brand_id).__name__}.")

    brand = repository.get_by_id(brand_id)
    if brand is None:
        raise UnableToFindIdError(
            entity_name="Brand",
            entity_id=brand_id
        )
        
    return brand.as_resource()
