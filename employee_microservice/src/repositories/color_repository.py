# External Library imports
from typing import Optional, List

# Internal library imports
from src.entities import ColorEntity
from src.repositories.base_repository import BaseRepository


class ColorRepository(BaseRepository):

    def get_all(self, limit: Optional[int] = None) -> List[ColorEntity]:
        """
        Retrieves all colors from the Employee MySQL database.
        
        :param limit: The maximum number of colors to retrieve (optional).
        :type limit: int | None
        :return: A list of ColorEntity objects.
        :rtype: list[ColorEntity]
        """
        colors_query = self.session.query(ColorEntity)
        if self.limit_is_valid(limit):
            colors_query = colors_query.limit(limit)
        return colors_query.all()


    def get_by_id(self, color_id: str) -> Optional[ColorEntity]:
        """
        Retrieves a color by ID from the Employee MySQL database.
        
        :param color_id: The ID of the color to retrieve.
        :type color_id: str
        :return: The color if found, None otherwise.
        :rtype: ColorEntity | None
        """
        return self.session.get(ColorEntity, color_id)
