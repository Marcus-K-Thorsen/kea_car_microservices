"""
**Color Repository Module**

This module defines the `ColorRepository` class, which provides methods for interacting
with the MongoDB collection for colors. It extends the `BaseRepository` class and
implements color-specific database operations.

Key Responsibilities:

- Retrieve all colors with optional limits.
- Retrieve a specific color by its ID.
"""

# External Library imports
from typing import Optional, List, Dict, Any
from pymongo.cursor import Cursor

# Internal library imports
from src.entities import ColorEntity
from src.repositories.base_repository import BaseRepository


class ColorRepository(BaseRepository):
    """
    Repository for managing color-related database operations.

    This class provides methods to interact with the MongoDB collection for colors,
    including retrieving all colors or a specific color by its ID.
    """

    def get_all(self, limit: Optional[int] = None) -> List[ColorEntity]:
        """
        Retrieves all colors from the database, with an optional limit.

        This method queries the MongoDB collection for colors and returns a list
        of `ColorEntity` objects. If a limit is provided, the number of results
        is restricted to the specified value.

        :param limit: The maximum number of colors to retrieve (optional).
        :type limit: int | None
        :return: A list of `ColorEntity` objects.
        :rtype: List[ColorEntity]
        """
        colors_collection = self.get_colors_collection()
        colors_query: Cursor[Dict[str, Any]] = colors_collection.find()
        
        if self.limit_is_valid(limit):
            colors_query = colors_query.limit(limit)
        
        return [ColorEntity(**color) for color in colors_query]

    def get_by_id(self, color_id: str) -> Optional[ColorEntity]:
        """
        Retrieves a specific color by its ID.

        This method queries the MongoDB collection for a color with the given ID
        and returns it as a `ColorEntity` object. If no color is found, it returns `None`.

        :param color_id: The ID of the color to retrieve.
        :type color_id: str
        :return: The `ColorEntity` object if found, otherwise `None`.
        :rtype: ColorEntity | None
        """
        colors_collection = self.get_colors_collection()
        color_query = colors_collection.find_one({"_id": color_id})
        
        if color_query is not None:
            return ColorEntity(**color_query)
        
        return None
