# Internal library imports
from src.entities.base_entity import BaseEntity


class AccessoryBaseEntity(BaseEntity):
    name: str
    price: float
    
class AccessoryEntity(AccessoryBaseEntity):
    pass

class AccessoryMessage(AccessoryBaseEntity):
    pass