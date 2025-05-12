# External Library imports

# Internal Library imports
from src.entities.base_entity import BaseEntity
from src.resources import EmployeeReturnResource


class EmployeeEntity(BaseEntity):
    email: str
    hashed_password: str
    first_name: str
    last_name: str
    role: str

    def as_resource(self) -> EmployeeReturnResource:
        return EmployeeReturnResource(
            id=self.id,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            role=self.role
        )