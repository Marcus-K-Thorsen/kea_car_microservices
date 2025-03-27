from pydantic import BaseModel, ConfigDict, Field


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

    
class InsuranceReturnResource(InsuranceBaseResource):
    id: str = Field(
        default=...,
        description="The UUID for the insurance.",
        examples=["8456043d-5fb0-49bf-ac2c-51567a32cc87"]
    )
