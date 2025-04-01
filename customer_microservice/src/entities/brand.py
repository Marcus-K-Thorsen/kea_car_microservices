"""
**Brand Entity Module**

This module defines the `BrandEntity` class, which represents a car brand in the system.
It extends the `BaseEntity` class and includes additional fields specific to brands,
such as `name` and `logo_url`.

Key Responsibilities:
- Define the structure of a brand entity.
- Provide a method to convert the entity into a resource representation (`BrandReturnResource`).
"""

# Internal library imports
from src.entities.base_entity import BaseEntity
from src.resources import BrandReturnResource


class BrandEntity(BaseEntity):
    """
    Represents a car brand entity in the Customer MongoDB system.

    This class extends the `BaseEntity` class and adds fields specific to car brands,
    such as `name` and `logo_url`. It also provides a method to convert the entity
    into a resource representation for API responses.

    Attributes:
        name (str): The name of the brand.
        logo_url (str): The URL of the brand's logo.
    """
    name: str
    logo_url: str

    def as_resource(self) -> BrandReturnResource:
        """
        Converts the `BrandEntity` into a `BrandReturnResource`.

        This method is used to transform the internal representation of a car brand
        into a format suitable for API responses.

        :return: A resource representation of the car brand.
        :rtype: BrandReturnResource
        """
        return BrandReturnResource(
            id=self.id,
            name=self.name,
            logo_url=self.logo_url,
        )