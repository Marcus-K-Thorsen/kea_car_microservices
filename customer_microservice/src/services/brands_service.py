"""
**Brands Service Module**

This module provides business logic for brand-related operations.
It interacts with the `BrandRepository` to retrieve data from the database
and transforms it into resource representations for API responses.

Key Responsibilities:

- Retrieve all car brands with optional limits.
- Retrieve a specific car brand by its ID.
"""

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
    """
    Retrieves all car brands from the database, with an optional limit.

    This function interacts with the `BrandRepository` to fetch brand data
    and converts it into a list of `BrandReturnResource` objects.

    :param database: The database connection instance.
    :type database: Database
    :param brands_limit: The maximum number of brands to retrieve (optional).
    :type brands_limit: int | None
    :return: A list of brands as `BrandReturnResource`.
    :rtype: List[BrandReturnResource]
    :raises TypeError: If `brands_limit` is not of type `int` or `None`.
    """
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
    """
    Retrieves a specific car brand by its ID.

    This function interacts with the `BrandRepository` to fetch a single brand
    and converts it into a `BrandReturnResource` object.

    :param database: The database connection instance.
    :type database: Database
    :param brand_id: The ID of the brand to retrieve.
    :type brand_id: str
    :return: The brand as a `BrandReturnResource`.
    :rtype: BrandReturnResource
    :raises TypeError: If `brand_id` is not of type `str`.
    :raises UnableToFindIdError: If no brand is found with the given ID.
    """
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
