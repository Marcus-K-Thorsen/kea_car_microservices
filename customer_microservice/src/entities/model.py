"""
**Model Entity Module**

This module defines the `ModelEntity` class, which represents a car model in the system.
It extends the `BaseEntity` class and includes additional fields specific to car models,
such as `name`, `price`, `image_url`, and relationships to `BrandEntity` and `ColorEntity`.

Key Responsibilities:

- Define the structure of a car model entity.
- Provide a method to convert the entity into a resource representation (`ModelReturnResource`).
"""

# External Library imports
from typing import List

# Internal library imports
from src.entities.base_entity import BaseEntity
from src.entities import BrandEntity, ColorEntity
from src.resources import ModelReturnResource


class ModelEntity(BaseEntity):
    """
    Represents a car model entity in the Customer MongoDB system.

    This class extends the `BaseEntity` class and adds fields specific to car models,
    such as `name`, `price`, `image_url`, and relationships to `BrandEntity` and `ColorEntity`.
    It also provides a method to convert the entity into a resource representation
    for API responses.

    Attributes:
        name (str): The name of the car model.
        price (float): The price of the car model.
        image_url (str): The URL of the car model's image.
        brand (BrandEntity): The brand associated with the car model.
        colors (List[ColorEntity]): The available colors for the car model.
    """
    name: str
    price: float
    image_url: str
    brand: BrandEntity
    colors: List[ColorEntity]

    def as_resource(self) -> ModelReturnResource:
        """
        Converts the `ModelEntity` into a `ModelReturnResource`.

        This method is used to transform the internal representation of a car model
        into a format suitable for API responses. It includes the brand and colors
        as nested resources.

        :return: A resource representation of the car model.
        :rtype: ModelReturnResource
        """
        return ModelReturnResource(
            id=self.id,
            brand=self.brand.as_resource(),
            colors=[color.as_resource() for color in self.colors],
            name=self.name,
            price=self.price,
            image_url=self.image_url,
        )
