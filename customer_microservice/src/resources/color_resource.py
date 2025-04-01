"""
**Color Resource Module**

This module defines the `ColorReturnResource` class, which represents the structure
of color-related API responses. It includes fields such as `id`, `name`, `price`, and RGB values.

Key Responsibilities:

- Define the structure of color-related API responses.
- Provide validation and documentation for color fields.
"""

from pydantic import BaseModel, ConfigDict, Field


class ColorReturnResource(BaseModel):
    """
    Represents a color in API responses.

    This class defines the fields for a color, including its unique identifier (`id`),
    name, price, and RGB values.

    Attributes:
        id (str): The UUID of the color.
        name (str): The name of the color.
        price (float): The price of the color in dollars.
        red_value (int): The red RGB value for the color (0-255).
        green_value (int): The green RGB value for the color (0-255).
        blue_value (int): The blue RGB value for the color (0-255).
    """

    id: str = Field(
        default=...,
        description="The UUID for the color.",
        examples=["5e755eb3-0099-4cdd-b064-d8bd95968109"]
    )
    name: str = Field(
        default=...,
        description="Name of the color.",
        examples=["blue"]
    )
    price: float = Field(
        default=...,
        description="Price of the color in dollars.",
        examples=[99.95]
    )
    red_value: int = Field(
        default=...,
        ge=0, le=255,
        description="The red RGB value for the color.",
        examples=[0]
    )
    green_value: int = Field(
        default=...,
        ge=0, le=255,
        description="The green RGB value for the color.",
        examples=[0]
    )
    blue_value: int = Field(
        default=...,
        ge=0, le=255,
        description="The blue RGB value for the color.",
        examples=[255]
    )

    model_config = ConfigDict(from_attributes=True)
    