# External Library imports
from typing import List

# Internal library imports
from src.entities.base_entity import BaseEntity
from src.entities import BrandEntity, ColorEntity

class ModelBaseEntity(BaseEntity):
    name: str
    price: float
    image_url: str
    

class ModelEntity(ModelBaseEntity):
    brand: BrandEntity
    colors: List[ColorEntity]
    
class ModelMessage(ModelBaseEntity):
    brand_id: str
    color_ids: List[str]
