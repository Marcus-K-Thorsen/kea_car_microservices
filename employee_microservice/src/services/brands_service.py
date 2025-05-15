# External Library imports
from typing import List, Optional

# Internal library imports
from src.database_management import Session
from src.exceptions import UnableToFindIdError
from src.repositories import BrandRepository
from src.resources import BrandReturnResource
from src.core import (
    TokenPayload,
    get_current_employee
)


def get_all(
        session: Session,
        token: TokenPayload,
        brand_limit: Optional[int] = None
) -> List[BrandReturnResource]:

    repository = BrandRepository(session)
    
    if isinstance(brand_limit, bool) or not (isinstance(brand_limit, int) or brand_limit is None):
        raise TypeError(f"brand_limit must be of type int or None, "
                        f"not {type(brand_limit).__name__}.")
        
    get_current_employee(token, session, current_user_action="get_all brands")

    brands = repository.get_all(limit=brand_limit)
    
    return [brand.as_resource() for brand in brands]


def get_by_id(
        session: Session,
        token: TokenPayload,
        brand_id: str
) -> BrandReturnResource:

    repository = BrandRepository(session)
    
    if not isinstance(brand_id, str):
        raise TypeError(f"brand_id must be of type str, "
                        f"not {type(brand_id).__name__}.")
    
    get_current_employee(token, session, current_user_action="get brand by id")

    brand = repository.get_by_id(brand_id)
    
    if brand is None:
        raise UnableToFindIdError(
            entity_name="Brand",
            entity_id=brand_id
        )
        
    return brand.as_resource()
