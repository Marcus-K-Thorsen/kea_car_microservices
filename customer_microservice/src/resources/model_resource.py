# External Library imports
from typing import List
from pydantic import BaseModel, ConfigDict, Field

# Internal library imports
from src.resources import BrandReturnResource
from src.resources import ColorReturnResource


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
    image_url: str = Field(
        default=...,
        description="URL from digitaloceanspaces for the model image.",
        examples=["https://keacar.ams3.cdn.digitaloceanspaces.com/Series_1.png"]
    )
    
    model_config = ConfigDict(from_attributes=True)


class ModelReturnResource(ModelBaseResource):
    id: str = Field(
        default=...,
        description="The UUID for the model.",
        examples=["ed996516-a141-4f4e-8991-3edeaba81c14"]
    )
    
    brand: BrandReturnResource = Field(
        default=...,
        description="The model's Brand as a BrandReturnResource."
    )
    
    colors: List[ColorReturnResource] = Field(
        default=...,
        description="The model's Colors as a list of ColorReturnResource."
    )
    