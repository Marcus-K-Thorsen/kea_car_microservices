# External Library imports


# Internal library imports
from src.entities.base_entity import BaseEntity
from src.resources import ColorReturnResource


class ColorEntity(BaseEntity):
    name: str
    price: float
    red_value: int
    green_value: int
    blue_value: int

    def as_resource(self) -> ColorReturnResource:
        return ColorReturnResource(
            id=self.id,
            name=self.name,
            price=self.price,
            red_value=self.red_value,
            green_value=self.green_value,
            blue_value=self.blue_value,
        )