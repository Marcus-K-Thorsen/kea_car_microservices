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
