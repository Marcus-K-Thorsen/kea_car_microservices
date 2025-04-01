"""
**Accessory Entity Module**

This module defines the `AccessoryEntity` class, which represents an accessory in the system.
It extends the `BaseEntity` class and includes additional fields specific to accessories,
such as `name` and `price`.

Key Responsibilities:

- Define the structure of an accessory entity.
- Provide a method to convert the entity into a resource representation (`AccessoryReturnResource`).
"""

# Internal library imports
from src.entities.base_entity import BaseEntity
from src.resources import AccessoryReturnResource


class AccessoryEntity(BaseEntity):
    """
    Represents an accessory entity in the Customer MongoDB system.

    This class extends the `BaseEntity` class and adds fields specific to accessories,
    such as `name` and `price`. It also provides a method to convert the entity into
    a resource representation for API responses.

    Attributes:
        name (str): The name of the accessory.
        price (float): The price of the accessory in dollars.
    """
    name: str
    price: float

    def as_resource(self) -> AccessoryReturnResource:
        """
        Converts the `AccessoryEntity` into an `AccessoryReturnResource`.

        This method is used to transform the internal representation of an accessory
        into a format suitable for API responses.

        :return: A resource representation of the accessory.
        :rtype: AccessoryReturnResource
        """
        return AccessoryReturnResource(
            id=self.id,
            name=self.name,
            price=self.price
        )
