# External Library imports
from enum import Enum
from typing import Any
from uuid import uuid4
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, UUID4

# Internal library imports
from src.logger_tool import log_and_raise_error

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
    
class EmployeeCreateOrUpdateResource(EmployeeBaseResource):
    email: EmailStr = Field(
        default=...,
        description="Email of the employee to create.",
        examples=["new@gmail.com"]
    )
    first_name: str = Field(
        default=...,
        description="First name of the employee to create.",
        examples=["New"]
    )
    last_name: str = Field(
        default=...,
        description="Last name of the employee to create.",
        examples=["Employee"]
    )
    
    role: RoleEnum = Field(
        default=...,
        description="Role of the employee to create.",
        examples=["manager"]
    )
    
    password: str = Field(
        default=...,
        description="Password of the employee to create.", 
        examples=["supersecretpassword125674"]
    )

    @field_validator('email')
    def validate_email(cls, email: str) -> str:
        minimum_length_of_email = 8
        maximum_length_of_email = 100
        email_length = len(email)
        if email_length < minimum_length_of_email:
            log_and_raise_error(f"The given email {email} is too short, "
                                f"it must be at least {minimum_length_of_email} characters long.")
        if email_length > maximum_length_of_email:
            log_and_raise_error(f"The given email {email} is {email_length - maximum_length_of_email} characters too long, "
                                f"it can only be maximum {maximum_length_of_email} characters and not {email_length}.")
        return email

    @field_validator('first_name')
    def validate_first_name(cls, first_name: str) -> str:
        minimum_length_of_first_name = 1
        maximum_length_of_first_name = 50
        first_name = first_name.strip()
        if len(first_name) < minimum_length_of_first_name:
            log_and_raise_error(f"The given first name {first_name} is too short, "
                                f"it must be at least {minimum_length_of_first_name} characters long.")
        if len(first_name) > maximum_length_of_first_name:
            log_and_raise_error(f"The given first name {first_name} is too long, "
                                f"it can only be maximum {maximum_length_of_first_name} characters long.")
        if '  ' in first_name:
            log_and_raise_error(f"The given first name {first_name} contains extra whitespaces.")
        if not all(part.isalpha() for part in first_name.replace('-', ' ').split()):
            log_and_raise_error(f"The given first name {first_name} can only contain alphabetic characters.")
        if first_name.startswith('-') or first_name.endswith('-'):
            log_and_raise_error(f"The given first name {first_name} starts or ends with a hyphen.")
        if ' -' in first_name or '- ' in first_name:
            log_and_raise_error(f"The given first name {first_name} contains whitespace before or after a hyphen.")
        return first_name.title()

    @field_validator('last_name')
    def validate_last_name(cls, last_name: str) -> str:
        minimum_length_of_last_name = 1
        maximum_length_of_last_name = 50
        last_name = last_name.strip()
        if len(last_name) < minimum_length_of_last_name:
            log_and_raise_error(f"The given last name {last_name} is too short, "
                             f"it must be at least {minimum_length_of_last_name} characters long.")
        if len(last_name) > maximum_length_of_last_name:
            log_and_raise_error(f"The given last name {last_name} is too long, "
                             f"it can only be maximum {maximum_length_of_last_name} characters long.")
        if ' ' in last_name:
            log_and_raise_error(f"The given last name {last_name} contains whitespace.")
        if not all(part.isalpha() for part in last_name.replace('-', ' ').split()):
            log_and_raise_error(f"The given last name {last_name} can only contain alphabetic characters.")
        if last_name.startswith('-') or last_name.endswith('-'):
            log_and_raise_error(f"The given last name {last_name} starts or ends with a hyphen.")
        return last_name.title()
    

    @field_validator('password')
    def validate_password(cls, password: str) -> str:
        maximum_length_of_password = 30
        if ' ' in password:
            log_and_raise_error(f"The given password {password} contains whitespaces.")
        if len(password) > maximum_length_of_password:
            log_and_raise_error(f"The given password {password} is too long, "
                             f"it can only be maximum {maximum_length_of_password} characters long.")
        
        return password

class EmployeeCreateResource(EmployeeCreateOrUpdateResource):
    """
    Resource for creating a new employee.
    """
    id: UUID4 = Field(
        default_factory=uuid4,
        description="ID of the employee to create.",
        examples=[uuid4()]
    )


class EmployeeUpdateResource(EmployeeCreateOrUpdateResource):
    """
    Resource for updating an existing employee.
    """
    email: EmailStr = Field(
        default=None,
        description="Email of the employee to update.",
        examples=["updated@gmail.com"]
    )
    first_name: str = Field(
        default=None,
        description="First name of the employee to update.",
        examples=["Donald"]
    )
    last_name: str = Field(
        default=None,
        description="Last name of the employee to update.",
        examples=["Duck"]
    )
    role: RoleEnum = Field(
        default=None,
        description="Role of the employee to update.",
        examples=["sales_person"]
    )
    password: str = Field(
        default=None,
        description="Password of the employee to update.",
        examples=["newsrecretp@ssword135"]
    )
    
    def get_updated_fields(self) -> dict[str, Any]:
        return self.model_dump(exclude_unset=True)
    

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
    