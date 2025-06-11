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
    
    def to_mongo_dict(self, exlude_id: bool) -> dict:
        """Convert the entity to a dictionary suitable for MongoDB."""
        data = super().to_mongo_dict(exlude_id=exlude_id)
        data["brand"] = self.brand.to_mongo_dict(exlude_id)
        data["colors"] = [color.to_mongo_dict(exlude_id) for color in self.colors]
        return data
    
class ModelMessage(ModelBaseEntity):
    brands_id: str
    color_ids: List[str]
