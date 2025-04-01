"""
**Colors Service Module**

This module provides business logic for color-related operations.
It interacts with the `ColorRepository` to retrieve data from the database
and transforms it into resource representations for API responses.

Key Responsibilities:

- Retrieve all colors with optional limits.
- Retrieve a specific color by its ID.
"""

# External Library imports
from typing import List, Optional

# Internal library imports
from src.database_management import Database
from src.repositories import ColorRepository
from src.resources import ColorReturnResource
from src.exceptions import UnableToFindIdError


def get_all(
        database: Database,
        colors_limit: Optional[int] = None
) -> List[ColorReturnResource]:
    """
    Retrieves all colors from the database, with an optional limit.

    This function interacts with the `ColorRepository` to fetch color data
    and converts it into a list of `ColorReturnResource` objects.

    :param database: The database connection instance.
    :type database: Database
    :param colors_limit: The maximum number of colors to retrieve (optional).
    :type colors_limit: int | None
    :return: A list of colors as `ColorReturnResource`.
    :rtype: List[ColorReturnResource]
    :raises TypeError: If `colors_limit` is not of type `int` or `None`.
    """
    repository = ColorRepository(database)
    
    if isinstance(colors_limit, bool) or not (isinstance(colors_limit, int) or colors_limit is None):
        raise TypeError(f"colors_limit must be of type int or None, "
                        f"not {type(colors_limit).__name__}.")

    colors = repository.get_all(limit=colors_limit)
    
    return [color.as_resource() for color in colors]
    

def get_by_id(
        database: Database,
        color_id: str
) -> ColorReturnResource:
    """
    Retrieves a specific color by its ID.

    This function interacts with the `ColorRepository` to fetch a single color
    and converts it into a `ColorReturnResource` object.

    :param database: The database connection instance.
    :type database: Database
    :param color_id: The ID of the color to retrieve.
    :type color_id: str
    :return: The color as a `ColorReturnResource`.
    :rtype: ColorReturnResource
    :raises TypeError: If `color_id` is not of type `str`.
    :raises UnableToFindIdError: If no color is found with the given ID.
    """
    repository = ColorRepository(database)
    
    if not isinstance(color_id, str):
        raise TypeError(f"color_id must be of type str, "
                        f"not {type(color_id).__name__}.")

    color = repository.get_by_id(color_id)
    if color is None:
        raise UnableToFindIdError(
            entity_name="Color",
            entity_id=color_id
        )
        
    return color.as_resource()
