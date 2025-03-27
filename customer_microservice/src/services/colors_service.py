# External Library imports
from typing import List, Optional
from pymongo.database import Database

# Internal library imports
from src.repositories import ColorRepository
from src.resources import ColorReturnResource
from src.exceptions import UnableToFindIdError


def get_all(
        database: Database,
        colors_limit: Optional[int] = None
) -> List[ColorReturnResource]:

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

