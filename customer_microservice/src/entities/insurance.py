# External Library imports


# Internal library imports
from src.entities.base_entity import BaseEntity
from src.resources import InsuranceReturnResource


class InsuranceEntity(BaseEntity):
    name: str
    price: float


    def as_resource(self) -> InsuranceReturnResource:
        return InsuranceReturnResource(
            id=self.id,
            name=self.name,
            price=self.price
        )
