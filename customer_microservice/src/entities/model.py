# External Library imports
from typing import List

# Internal library imports
from src.entities.base_entity import BaseEntity
from src.entities import BrandEntity, ColorEntity
from src.resources import ModelReturnResource


class ModelEntity(BaseEntity):
    name: str
    price: float
    image_url: str
    brand: BrandEntity
    colors: List[ColorEntity]

    def as_resource(self) -> ModelReturnResource:
        return ModelReturnResource(
            id=self.id,
            brand=self.brand.as_resource(),
            colors=[color.as_resource() for color in self.colors],
            name=self.name,
            price=self.price,
            image_url=self.image_url,
        )
