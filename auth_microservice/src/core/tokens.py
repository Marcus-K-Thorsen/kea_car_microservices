# External Library imports
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, Field


# Internal library imports
from src.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.resources import EmployeeReturnResource


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


class TokenData(BaseModel):
    sub: str = Field(default=...)
    exp: datetime = Field(
        default_factory=lambda: ((datetime.now(timezone.utc) + timedelta(
            minutes=(ACCESS_TOKEN_EXPIRE_MINUTES if ACCESS_TOKEN_EXPIRE_MINUTES is not None else 15)
        )))
    )