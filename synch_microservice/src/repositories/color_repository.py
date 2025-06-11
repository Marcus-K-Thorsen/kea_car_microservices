# External Library imports
from typing import Optional

# Internal library imports
from src.entities import ColorEntity
from src.repositories.base_repository import BaseRepository


class ColorRepository(BaseRepository):
    def get_by_id(self, color_id: str) -> Optional[ColorEntity]:
        """
        Retrieves a specific color by its ID from the Customer Mongo database.

        This method queries the MongoDB collection for a color with the given ID
        and returns it as an `ColorEntity` object. If no color is found, it
        returns `None`.

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
    