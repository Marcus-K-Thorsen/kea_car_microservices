# External Library imports
import json
from enum import Enum
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase

class BaseEntity(DeclarativeBase):
    def to_dict(self):
        """Convert the ORM object to a dictionary."""
        return {column.key: getattr(self, column.key) for column in self.__table__.columns}

    def to_json(self) -> str:
        """Convert the entity to a JSON-compatible byte string."""
        def custom_serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()  # Convert datetime to ISO 8601 string
            if isinstance(obj, Enum):
                return obj.value  # Convert Enum to its value
            raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

        return json.dumps(self.to_dict(), default=custom_serializer)
    
    def to_bytes(self) -> bytes:
        """Convert the entity to a byte string."""
        return self.to_json().encode('utf-8')
