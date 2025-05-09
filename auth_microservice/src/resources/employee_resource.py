# External Library imports
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime

# Internal library imports



class EmployeeBaseResource(BaseModel):
    id: str = Field(
        default=...,
        description="ID of the employee.",
        examples=["f9097a97-eca4-49b6-85a0-08423789c320"]
    )
    email: str = Field(
        default=...,
        description="Email of the employee.",
        examples=["hans@gmail.com"]
    )
    first_name: str = Field(
        default=...,
        description="First name of the employee.",
        examples=["Hans"]
    )
    last_name: str = Field(
        default=...,
        description="Last name of the employee.",
        examples=["Hansen"]
    )
    role: str = Field(
        default=...,
        description="Role of the employee.",
        examples=["manager"]
    )
    
    
    model_config = ConfigDict(from_attributes=True)
    
class EmployeeCreateOrUpdateResource(EmployeeBaseResource):
    hashed_password: str
    created_at: datetime
    updated_at: datetime



class EmployeeReturnResource(EmployeeBaseResource):
    """
    Resource for returning employee data.
    """
    is_deleted: bool = Field(
        default=False,
        description="Indicates if the employee is deleted.",
        examples=[False]
    )
    
    @field_validator("is_deleted")
    def check_is_deleted(cls, is_deleted: bool) -> bool:
        if is_deleted is True:
            is_deleted = False
        return is_deleted
    