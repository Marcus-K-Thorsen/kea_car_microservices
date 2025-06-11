# External Library imports
from uuid import uuid4
from datetime import date
from pydantic import BaseModel, ConfigDict, Field, UUID4, field_validator

# Internal library imports
from src.resources.car_resource import CarReturnResource


class PurchaseBaseResource(BaseModel):
    date_of_purchase: date = Field(
        default=...,
        description="The date of the purchase for when the purchase was made.",
        examples=[date.today()]
    )

    model_config = ConfigDict(from_attributes=True)

class PurchaseCreateResource(PurchaseBaseResource):
    id: UUID4 = Field(
        default_factory=uuid4,
        description="The UUID for the purchase to create.",
        examples=[uuid4()]
    )
    
    date_of_purchase: date = Field(
        default_factory=date.today,
        description="The date of the purchase for when the purchase was made.",
        examples=[date.today()]
    )

    cars_id: UUID4 = Field(
        default=...,
        description="UUID of the Car that the purchase belongs to.",
        examples=["e7bd48c2-f1c4-4e1a-b0fc-dc09f2d8f28a"]
    )

    @field_validator("date_of_purchase")
    def validate_date_of_purchase(cls, date_of_purchase: date) -> date:
        current_date = date.today()
        minimum_date_of_purchase = date(2023, 1, 1)
        
        if date_of_purchase < minimum_date_of_purchase:
            raise ValueError(f"The date: {date_of_purchase.strftime('%d-%m-%Y')} of purchase "
                             f"cannot be before {minimum_date_of_purchase.strftime('%d-%m-%Y')}.")
        if date_of_purchase > current_date:
            raise ValueError(f"The date: {date_of_purchase.strftime('%d-%m-%Y')} of purchase "
                             f"cannot be in the future.")
        
        return date_of_purchase


class PurchaseReturnResource(PurchaseBaseResource):
    id: str = Field(
        default=...,
        description="UUID of the purchase.",
        examples=["e7bd48c2-f1c4-4e1a-b0fc-dc09f2d8f28a"]
    )
    
    car: CarReturnResource = Field(
        default=...,
        description="The purchase's Car as a CarReturnResource."
    )
