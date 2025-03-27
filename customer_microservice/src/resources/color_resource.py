from pydantic import BaseModel, ConfigDict, Field

class ColorBaseResource(BaseModel):
    name: str = Field(
        default=...,
        description="Name of the color.",
        examples=["blue"]
    )
    price: float = Field(
        default=...,
        description="Price of the color in dollars.",
        examples=[99.95]
    )
    red_value: int = Field(
        default=...,
        ge=0, le=255,
        description="The red RGB value for the color.",
        examples=[0]
    )
    green_value: int = Field(
        default=...,
        ge=0, le=255,
        description="The green RGB value for the color.", examples=[0]
    )
    blue_value: int = Field(
        default=...,
        ge=0, le=255,
        description="The blue RGB value for the color.",
        examples=[255]
    )
    
    model_config = ConfigDict(from_attributes=True)


class ColorReturnResource(ColorBaseResource):
    id: str = Field(
        default=...,
        description="The UUID for the color.",
        examples=["5e755eb3-0099-4cdd-b064-d8bd95968109"]
    )
