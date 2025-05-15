from typing import Any
from pydantic import BaseModel, ConfigDict, Field, UUID4, field_validator


class InsuranceBaseResource(BaseModel):
    name: str = Field(
        default=...,
        description="Name of the insurance.",
        examples=["Flat Tire"]
    )
    price: float = Field(
        default=...,
        description="Price of the insurance in dollars.",
        examples=[9.95]
    )
    
    model_config = ConfigDict(from_attributes=True)


class InsuranceCreateOrUpdateResource(InsuranceBaseResource):
    name: str = Field(
        default=...,
        description="Name of the insurance to create.",
        examples=["Flat Tire"]
    )
    price: float = Field(
        default=...,
        gt=0,
        le=100000,
        description="Price of the insurance to create in dollars.",
        examples=[9.95]
    )
    
    @field_validator("name")
    def validate_name(cls, name: str) -> str:
        maximum_length = 45
        minimum_length = 3
        name = name.strip()
        name_length = len(name)
        if name_length == 0:
            raise ValueError("Name cannot be empty.")
        if '  ' in name:
            raise ValueError(f"Name '{name}' cannot contain multiple spaces.")
        # Strip leading/trailing spaces and capitalize each word
        name = " ".join(word.capitalize() for word in name.strip().split())
        if name_length < minimum_length:
            raise ValueError(
                f"Name '{name}' must be at least {minimum_length} characters long."
            )
        if name_length > maximum_length:
            raise ValueError(
                f"Name '{name}' must be at most {maximum_length} characters long."
            )
        return name

class InsuranceCreateResource(InsuranceCreateOrUpdateResource):
    id: UUID4 = Field(
        default=...,
        description="The UUID for the insurance to create.",
        examples=["8456043d-5fb0-49bf-ac2c-51567a32cc85"]
    )

class InsuranceUpdateResource(InsuranceCreateOrUpdateResource):
    name: str = Field(
        default=None,
        description="Name of the insurance to update.",
        examples=["Flat Tire"]
    )
    price: float = Field(
        default=None,
        gt=0,
        le=100000,
        description="Price of the insurance to update in dollars.",
        examples=[9.95]
    )
    
    def get_updated_fields(self) -> dict[str, Any]:
        return self.model_dump(exclude_unset=True)

class InsuranceReturnResource(InsuranceBaseResource):
    id: str = Field(
        default=...,
        description="The UUID for the insurance.",
        examples=["8456043d-5fb0-49bf-ac2c-51567a32cc87"]
    )
