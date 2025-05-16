# External Library imports
from typing import List, Optional

# Internal library imports
from src.database_management import Session
from src.exceptions import UnableToFindIdError
from src.repositories import ColorRepository
from src.resources import ColorReturnResource
from src.core import (
    TokenPayload, 
    get_current_employee
)

def get_all(
        session: Session,
        token: TokenPayload,
        color_limit: Optional[int] = None
) -> List[ColorReturnResource]:

    repository = ColorRepository(session)
    
    if isinstance(color_limit, bool) or not (isinstance(color_limit, int) or color_limit is None):
        raise TypeError(f"color_limit must be of type int or None, "
                        f"not {type(color_limit).__name__}.")

    get_current_employee(
        token,
        session,
        current_user_action="get_all colors"
    )
    
    colors = repository.get_all(limit=color_limit)
    
    return [color.as_resource() for color in colors]
    

def get_by_id(
        session: Session,
        token: TokenPayload,
        color_id: str
) -> ColorReturnResource:

    repository = ColorRepository(session)
    
    if not isinstance(color_id, str):
        raise TypeError(f"color_id must be of type str, "
                        f"not {type(color_id).__name__}.")
        
    get_current_employee(
        token,
        session,
        current_user_action="get color by id"
    )

    color = repository.get_by_id(color_id)
    if color is None:
        raise UnableToFindIdError(
            entity_name="Color",
            entity_id=color_id
        )
        
    return color.as_resource()
