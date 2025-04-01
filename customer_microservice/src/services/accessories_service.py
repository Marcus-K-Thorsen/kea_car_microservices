"""
**Accessories Service Module**

This module provides business logic for accessory-related operations.
It interacts with the `AccessoryRepository` to retrieve data from the database
and transforms it into resource representations for API responses.

Key Responsibilities:

- Retrieve all accessories with optional limits.
- Retrieve a specific accessory by its ID.
"""

# External Library imports
from typing import List, Optional

# Internal library imports
from src.database_management import Database
from src.exceptions import UnableToFindIdError
from src.repositories import AccessoryRepository
from src.resources import AccessoryReturnResource


def get_all(
        database: Database,
        accessory_limit: Optional[int] = None
) -> List[AccessoryReturnResource]:
    """
    Retrieves all accessories from the database, with an optional limit.

    This function interacts with the `AccessoryRepository` to fetch accessory data
    and converts it into a list of `AccessoryReturnResource` objects.

    :param database: The database connection instance.
    :type database: Database
    :param accessory_limit: The maximum number of accessories to retrieve (optional).
    :type accessory_limit: int | None
    :return: A list of accessories as `AccessoryReturnResource`.
    :rtype: List[AccessoryReturnResource]
    :raises TypeError: If `accessory_limit` is not of type `int` or `None`.
    """
    repository = AccessoryRepository(database)
    
    if isinstance(accessory_limit, bool) or not (isinstance(accessory_limit, int) or accessory_limit is None):
        raise TypeError(f"accessory_limit must be of type int or None, "
                        f"not {type(accessory_limit).__name__}.")
        
    accessories = repository.get_all(limit=accessory_limit)

    return [accessory.as_resource() for accessory in accessories]


def get_by_id(
        database: Database,
        accessory_id: str
) -> AccessoryReturnResource:
    """
    Retrieves a specific accessory by its ID.

    This function interacts with the `AccessoryRepository` to fetch a single accessory
    and converts it into an `AccessoryReturnResource` object.

    :param database: The database connection instance.
    :type database: Database
    :param accessory_id: The ID of the accessory to retrieve.
    :type accessory_id: str
    :return: The accessory as an `AccessoryReturnResource`.
    :rtype: AccessoryReturnResource
    :raises TypeError: If `accessory_id` is not of type `str`.
    :raises UnableToFindIdError: If no accessory is found with the given ID.
    """
    repository = AccessoryRepository(database)
    
    if not isinstance(accessory_id, str):
        raise TypeError(f"accessory_id must be of type str, "
                        f"not {type(accessory_id).__name__}.")

    accessory = repository.get_by_id(accessory_id)
    if accessory is None:
        raise UnableToFindIdError(
            entity_name="Accessory",
            entity_id=accessory_id
        )
    
    return accessory.as_resource()
