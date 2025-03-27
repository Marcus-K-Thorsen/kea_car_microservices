from pydantic import BaseModel, ConfigDict, Field

class AccessoryBaseResource(BaseModel):
    name: str = Field(
        default=...,
        description="Name of the accessory.",
        examples=["Adaptive Headlights"]
    )
    price: float = Field(
        default=...,
        description="Price of the accessory in dollars.",
        examples=[99.95]
    )
    
    model_config = ConfigDict(from_attributes=True)


class AccessoryReturnResource(AccessoryBaseResource):
    id: str = Field(
        default=...,
        description="The UUID of the accessory.",
        examples=["e620ec3c-625d-4bde-9b77-f7449b6352d5"]
    )
