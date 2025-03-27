# External Library imports
from typing import Optional, List, Dict, Any
from pymongo.cursor import Cursor

# Internal library imports
from src.entities import ColorEntity
from src.repositories.base_repository import BaseRepository


class ColorRepository(BaseRepository):

    def get_all(self, limit: Optional[int] = None) -> List[ColorEntity]:
        colors_collection = self.get_colors_collection()
        colors_query: Cursor[Dict[str, Any]] = colors_collection.find()
        
        if self.limit_is_valid(limit):
            colors_query = colors_query.limit(limit)
        
        return [ColorEntity(**color) for color in colors_query]

    def get_by_id(self, color_id: str) -> Optional[ColorEntity]:
        colors_collection = self.get_colors_collection()
        
        color_query = colors_collection.find_one({"_id": color_id})
        
        if color_query is not None:
            return ColorEntity(**color_query)
        
        return None
