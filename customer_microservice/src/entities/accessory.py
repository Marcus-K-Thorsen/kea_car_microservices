# External Library imports


# Internal library imports
from src.entities.base_entity import BaseEntity
from src.resources import AccessoryReturnResource


class AccessoryEntity(BaseEntity):
    name: str
    price: float
    
    def as_resource(self) -> AccessoryReturnResource:
        return AccessoryReturnResource(
            id=self.id,
            name=self.name,
            price=self.price
        )

