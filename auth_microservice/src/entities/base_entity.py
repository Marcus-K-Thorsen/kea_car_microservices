# External Library imports
from typing import Union
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator, Field

# Internal Library imports


def truncate_to_seconds(dt: datetime) -> datetime:
    """Truncate a datetime object to seconds."""
    return dt.replace(microsecond=0)

class BaseEntity(BaseModel):
    id: str = Field(default=..., alias="_id")
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
        
    