"""
**Insurance Resource Module**

This module defines the `InsuranceReturnResource` class, which represents the structure
of insurance-related API responses. It includes fields such as `id`, `name`, and `price`.

Key Responsibilities:

- Define the structure of insurance-related API responses.
- Provide validation and documentation for insurance fields.
"""

from pydantic import BaseModel, ConfigDict, Field


class InsuranceReturnResource(BaseModel):
    """
    Represents an insurance in API responses.

    This class defines the fields for an insurance, including its unique identifier (`id`),
    name, and price.

    Attributes:
        id (str): The UUID of the insurance.
        name (str): The name of the insurance.
        price (float): The price of the insurance in dollars.
    """

    id: str = Field(
        default=...,
        description="The UUID for the insurance.",
        examples=["8456043d-5fb0-49bf-ac2c-51567a32cc87"]
    )
    name: str = Field(
        default=...,
        description="Name of the insurance.",
        examples=["Flat Tire"]
    )
    price: float = Field(
        default=...,
        description="Price of the insurance in dollars.",
        examples=[9.95]
    )

    model_config = ConfigDict(from_attributes=True)
    