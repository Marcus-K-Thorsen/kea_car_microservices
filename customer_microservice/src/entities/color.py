"""
**Color Entity Module**

This module defines the `ColorEntity` class, which represents a color entity in the system.
It extends the `BaseEntity` class and includes additional fields specific to colors, such as
`name`, `price`, and RGB values (`red_value`, `green_value`, `blue_value`).

Key Responsibilities:

- Define the structure of a color entity.
- Provide a method to convert the entity into a resource representation (`ColorReturnResource`).
"""

# Internal library imports
from src.entities.base_entity import BaseEntity
from src.resources import ColorReturnResource


class ColorEntity(BaseEntity):
    """
    Represents a color entity in the Customer MongoDB system.

    This class extends the `BaseEntity` class and adds fields specific to colors,
    such as `name`, `price`, and RGB values (`red_value`, `green_value`, `blue_value`).
    It also provides a method to convert the entity into a resource representation
    for API responses.

    Attributes:
        name (str): The name of the color.
        price (float): The price of the color.
        red_value (int): The red component of the color.
        green_value (int): The green component of the color.
        blue_value (int): The blue component of the color.
    """
    name: str
    price: float
    red_value: int
    green_value: int
    blue_value: int

    def as_resource(self) -> ColorReturnResource:
        """
        Converts the `ColorEntity` into a `ColorReturnResource`.

        This method is used to transform the internal representation of a color
        into a format suitable for API responses.

        :return: A resource representation of the color.
        :rtype: ColorReturnResource
        """
        return ColorReturnResource(
            id=self.id,
            name=self.name,
            price=self.price,
            red_value=self.red_value,
            green_value=self.green_value,
            blue_value=self.blue_value,
        )
