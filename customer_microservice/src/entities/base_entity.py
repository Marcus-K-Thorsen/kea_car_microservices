"""
**Base Entity Module**

This module defines the `BaseEntity` class, which serves as the foundation for all MongoDB entities
in the system. It provides common fields (`id`, `created_at`, `updated_at`) and validation logic
for datetime fields.
"""

from typing import Union
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator, Field


class BaseEntity(BaseModel):
    """
    Base class for MongoDB entities.

    This class provides common fields and validation logic for entities stored in MongoDB.
    All other entity classes inherit from this base class.

    Attributes:
        id (str): The unique identifier for the entity, mapped to MongoDB's `_id` field.
        created_at (datetime): The timestamp when the entity was created.
        updated_at (datetime): The timestamp when the entity was last updated.
    """

    id: str = Field(default=..., alias="_id")
    created_at: datetime = Field(default=None)
    updated_at: datetime = Field(default=None)

    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def validate_iso_datetime(value: Union[str, datetime], field_name: str) -> datetime:
        """
        Validates and converts a datetime field to a `datetime` object.

        Ensures that if the value is a string, it is in ISO 8601 format. Raises a `ValueError`
        if the string is not a valid ISO 8601 datetime.

        :param value: The value to validate, either a string or a `datetime` object.
        :param field_name: The name of the field being validated (used in error messages).
        :return: A valid `datetime` object.
        """
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value)
            except ValueError:
                raise ValueError(f"Invalid ISO 8601 datetime string for {field_name}: {value}")
        return value

    @field_validator("created_at", mode="before")
    @classmethod
    def validate_created_at(cls, value: Union[str, datetime]) -> datetime:
        """
        Validates the `created_at` field.

        :param value: The value to validate, either a string or a `datetime` object.
        :return: A valid `datetime` object.
        """
        return cls.validate_iso_datetime(value, "created_at")

    @field_validator("updated_at", mode="before")
    @classmethod
    def validate_updated_at(cls, value: Union[str, datetime]) -> datetime:
        """
        Validates the `updated_at` field.

        :param value: The value to validate, either a string or a `datetime` object.
        :return: A valid `datetime` object.
        """
        return cls.validate_iso_datetime(value, "updated_at")
    