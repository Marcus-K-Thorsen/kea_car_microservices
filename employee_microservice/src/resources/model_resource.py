# External Library imports
from uuid import uuid4, UUID
from typing import List, Union
from fastapi import Form, File, UploadFile, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, field_validator, UUID4, ValidationError

# Internal library imports
from src.resources.brand_resource import BrandReturnResource
from src.resources.color_resource import ColorReturnResource


class ModelBaseResource(BaseModel):
    name: str = Field(
        default=...,
        description="Name of the model.",
        examples=["Series 1"]
    )
    price: float = Field(
        default=...,
        description="Price of the model in dollars.",
        examples=[10090.95]
    )
    
    
    model_config = ConfigDict(from_attributes=True)


class ModelCreateOrUpdateResource(ModelBaseResource):
    name: str = Field(
        default=...,
        description="Name of the model to create.",
        examples=["Series 2"]
    )
    price: float = Field(
        default=...,
        description="Price of the model to create in dollars.",
        examples=[10090.95]
    )
    brands_id: UUID4 = Field(
        default=...,
        description="The UUID of the brand to the model to create.",
        examples=["feb2efdb-93ee-4f45-88b1-5e4086c00334"]
    )
    color_ids: List[UUID4] = Field(
        default=...,
        exclude=True,
        description="List of UUID of the colors for the model to create.",
        examples=[
            [
                "14382aba-6fe6-405d-a5e2-0b8cfd1f9582", 
                "5e755eb3-0099-4cdd-b064-d8bd95968109", 
                "74251648-a7b1-492a-ab2a-f2248c58da00"
            ]
        ]
    )
    
    @field_validator("name")
    def validate_name(cls, name: str) -> str:
        name = name.strip()
        name_length = len(name)
        maximum_length = 60
        if name_length < 1:
            raise ValueError("Model name must be at least 1 character long.")
        if name_length > maximum_length:
            raise ValueError(
                f"The given Model name {name} is {name_length - maximum_length} characters too long, "
                f"it can only be maximum {maximum_length} characters and not {name_length}.")
        return name
    
    @field_validator("price")
    def validate_price(cls, price: float) -> float:
        if price <= 0:
            raise ValueError("Model price must be greater than 0.")
        if price > 10000000:
            raise ValueError("Model price must be less than 10,000,000.")
        return price
    
    @field_validator("color_ids")
    def validate_color_ids(cls, color_ids: List[UUID4]) -> List[UUID4]:
        amount_of_colors = len(color_ids)
        amount_of_unique_colors = len(set(color_ids))
        if amount_of_colors < 1:
            raise ValueError("Model must have at least 1 color.")
        if amount_of_colors != amount_of_unique_colors:
            raise ValueError("Model must not have duplicate colors.")
        return color_ids


class ModelCreateResource(ModelCreateOrUpdateResource):
    id: UUID4 = Field(
        default_factory=uuid4,
        description="ID of the model to create.",
        examples=[uuid4()]
    )


def model_as_form_with_file(
    id: UUID = Form(
        default_factory=uuid4,
        description="""ID of the model to create.""",
        examples=[uuid4()]
    ),
    name: str = Form(
        ...,
        description="""Name of the model to create.""",
        examples=["Series 3"]
    ),
    price: float = Form(
        ...,
        description="""Price of the model to create in dollars.""",
        examples=[19990.95]
    ),
    brands_id: UUID = Form(
        ...,
        description="""The UUID of the brand to the model to create.""",
        examples=["feb2efdb-93ee-4f45-88b1-5e4086c00334"]
    ),
    color_ids: Union[List[str], str] = Form(
        ...,
        description="List of UUIDs of the colors for the model to create, can be a single string with comma-separated values or a list of strings.",
        examples=[
            [
                "14382aba-6fe6-405d-a5e2-0b8cfd1f9582", 
                "5e755eb3-0099-4cdd-b064-d8bd95968109", 
                "74251648-a7b1-492a-ab2a-f2248c58da00"
            ]
        ]
    ),
    model_image: UploadFile = File(
        ...,
        description="""Image file for the model to create."""
    )
) -> tuple[ModelCreateResource, UploadFile]:
    prepared_color_ids: List[str] = []
    if isinstance(color_ids, str):
        # If a single string is provided, convert it to a list
        color_ids = color_ids.split(",")
        
    for color_id in color_ids:
        color_id = color_id.replace(" ", "")
        if len(color_id) > 0:
            for internal_color_id in color_id.split(","):
                internal_color_id = internal_color_id.strip()
                if len(internal_color_id) > 0:
                    prepared_color_ids.append(internal_color_id)
    try:
        return ModelCreateResource(
            id=id,
            name=name,
            price=price,
            brands_id=brands_id,
            color_ids=prepared_color_ids
            ), model_image
    except ValidationError as e:
        # This will make FastAPI return a 422 with the correct error details
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e.errors())
        )


class ModelUpdateResource(ModelCreateOrUpdateResource):
    name: str = Field(
        default=None,
        description="Name of the model to update.",
        examples=["Series 2"]
    )
    price: float = Field(
        default=None,
        description="Price of the model to update in dollars.",
        examples=[10090.95]
    )
    brands_id: UUID4 = Field(
        default=None,
        description="The UUID of the brand to the model to update.",
        examples=["feb2efdb-93ee-4f45-88b1-5e4086c00334"]
    )
    color_ids: List[UUID4] = Field(
        default=None,
        exclude=True,
        description="List of UUID of the colors for the model to update.",
        examples=[
            [
                "14382aba-6fe6-405d-a5e2-0b8cfd1f9582", 
                "5e755eb3-0099-4cdd-b064-d8bd95968109", 
                "74251648-a7b1-492a-ab2a-f2248c58da00"
            ]
        ]
    )
    
    def get_updated_fields(self) -> dict[str, str]:
        return self.model_dump(exclude_unset=True)

    
class ModelReturnResource(ModelBaseResource):
    
    id: str = Field(
        default=...,
        description="The UUID for the model.",
        examples=["ed996516-a141-4f4e-8991-3edeaba81c14"]
    )
    image_url: str = Field(
        default=...,
        description="URL from digitaloceanspaces for the model image.",
        examples=["https://keacar.ams3.cdn.digitaloceanspaces.com/Series_1.png"]
    )
    brand: BrandReturnResource = Field(
        default=...,
        description="The model's Brand as a BrandReturnResource."
    )
    colors: List[ColorReturnResource] = Field(
        default=...,
        description="The model's Colors as a list of ColorReturnResource."
    )
