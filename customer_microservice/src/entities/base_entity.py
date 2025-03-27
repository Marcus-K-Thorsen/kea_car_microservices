from typing import Union
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator, Field


class BaseEntity(BaseModel):
    id: str = Field(default=..., alias="_id")
    created_at: datetime = Field(default=None)
    updated_at: datetime = Field(default=None)

    model_config = ConfigDict(from_attributes=True)
    
    @staticmethod
    def validate_iso_datetime(value: Union[str, datetime], field_name: str) -> datetime:
        """
        Validates and converts a datetime field to a `datetime` object.
        Ensures that if the value is a string, it is in ISO 8601 format.
        """
        if isinstance(value, str):
            try:
                # Attempt to parse the string as an ISO 8601 datetime
                value = datetime.fromisoformat(value)
            except ValueError:
                raise ValueError(f"Invalid ISO 8601 datetime string for {field_name}: {value}")
        return value

    @field_validator("created_at", mode="before")
    @classmethod
    def validate_created_at(cls, value: Union[str, datetime]) -> datetime:
        return cls.validate_iso_datetime(value, "created_at")

    @field_validator("updated_at", mode="before")
    @classmethod
    def validate_updated_at(cls, value: Union[str, datetime]) -> datetime:
        return cls.validate_iso_datetime(value, "updated_at")
