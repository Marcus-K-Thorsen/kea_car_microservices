# External Library imports


# Internal library imports
from src.entities.base_entity import BaseEntity
from src.resources import BrandReturnResource


class BrandEntity(BaseEntity):
    name: str
    logo_url: str

    def as_resource(self) -> BrandReturnResource:
        return BrandReturnResource(
            id=self.id,
            name=self.name,
            logo_url=self.logo_url,
        )
