"""
**Brand Resource Module**

This module defines the `BrandReturnResource` class, which represents the structure
of car brand-related API responses. It includes fields such as `id`, `name`, and `logo_url`.

Key Responsibilities:

- Define the structure of brand-related API responses.
- Provide validation and documentation for brand fields.
"""

from pydantic import BaseModel, ConfigDict, Field


class BrandReturnResource(BaseModel):
    """
    Represents a brand in API responses.

    This class defines the fields for a car brand, including its unique identifier (`id`),
    name, and logo URL.

    Attributes:
        id (str): The UUID of the brand.
        name (str): The name of the brand.
        logo_url (str): The URL of the brand's logo.
    """

    id: str = Field(
        default=...,
        description="UUID of the brand.",
        examples=["feb2efdb-93ee-4f45-88b1-5e4086c00334"]
    )
    name: str = Field(
        default=...,
        description="Name of the brand.",
        examples=["BMW"]
    )
    logo_url: str = Field(
        default=...,
        description="URL from digitaloceanspaces for the brand logo.",
        examples=["https://keacar.ams3.cdn.digitaloceanspaces.com/bmw-logo.png"]
    )

    model_config = ConfigDict(from_attributes=True)
    