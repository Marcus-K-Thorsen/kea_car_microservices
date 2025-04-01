"""
**Model Resource Module**

This module defines the `ModelReturnResource` class, which represents the structure
of car model-related API responses. It includes fields such as `id`, `name`, `price`, `image_url`,
`brand`, and `colors`.

Key Responsibilities:

- Define the structure of car model-related API responses.
- Provide validation and documentation for car model fields.
"""

# External Library imports
from typing import List
from pydantic import BaseModel, ConfigDict, Field

# Internal library imports
from src.resources import BrandReturnResource
from src.resources import ColorReturnResource


class ModelReturnResource(BaseModel):
    """
    Represents a car model in API responses.

    This class defines the fields for a car model, including its unique identifier (`id`),
    name, price, image URL, associated brand, and available colors.

    Attributes:
        id (str): The UUID of the car model.
        name (str): The name of the car model.
        price (float): The price of the car model in dollars.
        image_url (str): The URL of the car model's image.
        brand (BrandReturnResource): The brand associated with the car model.
        colors (List[ColorReturnResource]): The available colors for the car model.
    """

    id: str = Field(
        default=...,
        description="The UUID for the model.",
        examples=["ed996516-a141-4f4e-8991-3edeaba81c14"]
    )
    name: str = Field(
        default=...,
        description="Name of the model.",
        examples=["Series 1"]
    )
    price: float = Field(
        default=...,
        description="Price of the model in dollars.",
        examples=[10090.95]
    )
    image_url: str = Field(
        default=...,
        description="URL from digitaloceanspaces for the model image.",
        examples=["https://keacar.ams3.cdn.digitaloceanspaces.com/Series_1.png"]
    )
    brand: BrandReturnResource = Field(
        default=...,
        description="The model's Brand as a BrandReturnResource."
    )
    colors: List[ColorReturnResource] = Field(
        default=...,
        description="The model's Colors as a list of ColorReturnResource."
    )

    model_config = ConfigDict(from_attributes=True)
    