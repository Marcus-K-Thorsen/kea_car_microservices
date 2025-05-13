# External Library imports
from enum import Enum
from pydantic import BaseModel, ConfigDict, EmailStr, Field

# Internal library imports


class EmployeeLoginResource(BaseModel):
    email: str = Field(
        default=...,
        description="Email of the employee to login as.",
        examples=["hans@gmail.com"]
    )
    password: str = Field(
        default=...,
        description="Password of the employee to login as.",
        examples=["hans123"]
    )


class RoleEnum(str, Enum):
    admin = "admin"
    manager = "manager"
    sales_person = "sales_person"
    

class EmployeeBaseResource(BaseModel):
    email: EmailStr = Field(
        default=...,
        description="Email of the employee.",
        examples=["tom@gmail.com"]
    )
    first_name: str = Field(
        default=...,
        description="First name of the employee.",
        examples=["Tom"]
    )
    last_name: str = Field(
        default=...,
        description="Last name of the employee.",
        examples=["Tomsen"]
    )
    role: RoleEnum = Field(
        default=...,
        description="Role of the employee.",
        examples=["admin"]
    )
    
    model_config = ConfigDict(from_attributes=True)
    

class EmployeeReturnResource(EmployeeBaseResource):
    """
    Resource for returning employee data.
    """
    id: str = Field(
        default=...,
        description="ID of the employee.",
        examples=["24bd8a11-2310-46bc-aebf-0887325ebdbd"]
    )
    is_deleted: bool = Field(
        default=...,
        description="Indicates if the employee is deleted.",
        examples=[False]
    )
    

    