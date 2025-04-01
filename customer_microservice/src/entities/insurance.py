"""
**Insurance Entity Module**

This module defines the `InsuranceEntity` class, which represents an insurance entity in the system.
It extends the `BaseEntity` class and includes additional fields specific to insurances, such as
`name` and `price`.

Key Responsibilities:

- Define the structure of an insurance entity.
- Provide a method to convert the entity into a resource representation (`InsuranceReturnResource`).
"""

# Internal library imports
from src.entities.base_entity import BaseEntity
from src.resources import InsuranceReturnResource


class InsuranceEntity(BaseEntity):
    """
    Represents an insurance entity in the Customer MongoDB system.

    This class extends the `BaseEntity` class and adds fields specific to insurances,
    such as `name` and `price`. It also provides a method to convert the entity into
    a resource representation for API responses.

    Attributes:
        name (str): The name of the insurance.
        price (float): The price of the insurance.
    """
    name: str
    price: float

    def as_resource(self) -> InsuranceReturnResource:
        """
        Converts the `InsuranceEntity` into an `InsuranceReturnResource`.

        This method is used to transform the internal representation of an insurance
        into a format suitable for API responses.

        :return: A resource representation of the insurance.
        :rtype: InsuranceReturnResource
        """
        return InsuranceReturnResource(
            id=self.id,
            name=self.name,
            price=self.price
        )
