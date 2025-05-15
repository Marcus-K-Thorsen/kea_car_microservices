# Internal library imports
from src.entities.base_entity import BaseEntity

class ColorBaseEntity(BaseEntity):
    name: str
    price: float
    red_value: int
    green_value: int
    blue_value: int


class ColorEntity(ColorBaseEntity):
    pass

class ColorMessage(ColorBaseEntity):
    pass