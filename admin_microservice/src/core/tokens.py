# External Library imports
from pydantic import BaseModel, Field
from datetime import timezone, datetime, timedelta


# Internal library imports



class TokenPayload(BaseModel):
    email: str = Field(
        default=...,
        description="The email of the employee that the token belongs to.",
        examples=["hans@gmail.com"]
    )
    expires_at: datetime = Field(
        default=...,
        description="The date and time as UTC for when the token expires.",
        examples=
        [
            (datetime.now(timezone.utc) + timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M:%S")
        ]
    )
