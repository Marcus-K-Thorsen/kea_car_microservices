# Internal library imports
from src.entities.base_entity import BaseEntity

class BrandBaseEntity(BaseEntity):
    name: str
    logo_url: str
    
class BrandEntity(BrandBaseEntity):
    pass

class BrandMessage(BrandBaseEntity):
    pass