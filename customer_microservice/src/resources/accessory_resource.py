"""
**Accessory Resource Module**

This module defines the `AccessoryReturnResource` class, which represents the structure
of accessory-related API responses. It includes fields such as `id`, `name`, and `price`.

Key Responsibilities:

- Define the structure of accessory-related API responses.
- Provide validation and documentation for accessory fields.
"""

from pydantic import BaseModel, ConfigDict, Field


class AccessoryReturnResource(BaseModel):
    """
    Represents an accessory in API responses.

    This class defines the fields for an accessory, including its unique identifier (`id`),
    name, and price.

    Attributes:
        id (str): The UUID of the accessory.
        name (str): The name of the accessory.
        price (float): The price of the accessory in dollars.
    """

    id: str = Field(
        default=...,
        description="The UUID of the accessory.",
        examples=["e620ec3c-625d-4bde-9b77-f7449b6352d5"]
    )
    name: str = Field(
        default=...,
        description="The name of the accessory.",
        examples=["Adaptive Headlights"]
    )
    price: float = Field(
        default=...,
        description="The price of the accessory in dollars.",
        examples=[99.95]
    )

    model_config = ConfigDict(from_attributes=True)
    