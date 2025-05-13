# External Library imports
import json
from enum import Enum
from typing import Union
from datetime import datetime, date
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel, ConfigDict, field_validator, Field

# Internal Library imports


def truncate_to_seconds(dt: datetime) -> datetime:
    """Truncate a datetime object to seconds."""
    return dt.replace(microsecond=0)


class BaseEntity(DeclarativeBase):
    def to_dict(self):
        """Convert the ORM object to a dictionary."""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.key)
            # Apply truncate_to_seconds to datetime fields
            if isinstance(value, datetime):
                value = truncate_to_seconds(value)
             # Convert date fields to ISO 8601 strings
            elif isinstance(value, date):
                value = value.isoformat()
            result[column.key] = value
        return result

    def to_json(self) -> str:
        """Convert the entity to a JSON-compatible byte string."""
        def custom_serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()  # Convert datetime to ISO 8601 string
            if isinstance(obj, date):
                return obj.isoformat()  # Convert date to ISO 8601 string
            if isinstance(obj, Enum):
                return obj.value  # Convert Enum to its value
            if isinstance(obj, bool):
                return obj
            raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

        return json.dumps(self.to_dict(), default=custom_serializer)
    
    def to_bytes(self) -> bytes:
        """Convert the entity to a byte string."""
        return self.to_json().encode('utf-8')
    


class BaseMessage(BaseModel):
    id: str = Field(default=...)
    created_at: datetime = Field(default=...)
    updated_at: datetime = Field(default=...)

    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def validate_iso_datetime(value: Union[str, datetime], field_name: str) -> datetime:
        if isinstance(value, str):
            try:
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
    
    def to_mongo_dict(self, exlude_id: bool) -> dict:
        """Convert the entity to a dictionary suitable for MongoDB."""
        if exlude_id:
            data = self.model_dump(by_alias=True, exclude={"_id"})
        else:
            data = self.model_dump(by_alias=True)
        data["created_at"] = truncate_to_seconds(self.created_at).isoformat()
        data["updated_at"] = truncate_to_seconds(self.updated_at).isoformat()
        return data
        
    