# External Library imports
from pydantic import BaseModel, Field
from datetime import timezone, datetime, timedelta


# Internal library imports
from src.resources import EmployeeReturnResource


class TokenPayload(BaseModel):
    employee_id: str = Field(
        default=...,
        description="The id of the employee that the token belongs to.",
        examples=["f9097a97-eca4-49b6-85a0-08423789c320"]
    )
    expires_at: datetime = Field(
        default=...,
        description="The date and time as UTC for when the token expires.",
        examples=
        [
            (datetime.now(timezone.utc) + timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M:%S")
        ]
    )


class Token(BaseModel):
    access_token: str = Field(
        default=...,
        description="The access token needed for accessing endpoints that requires authorization.",
        examples=[
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJzdWIiOiJzdXNhbiIsImV4cCI6MTcyOTE2NTEyOX0."
            "U1wCg1dyIX2U1dSjLHSpi3EGc99lXK1458G8j39TCiw"
        ]
    )
    token_type: str = Field(
        default=...,
        description="The type of token that is needed for authorization.",
        examples=["bearer"]
    )
    employee: EmployeeReturnResource = Field(
        default=...,
        description="The employee that the token belongs to."
    )