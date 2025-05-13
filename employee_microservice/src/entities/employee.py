# External Library imports
from datetime import datetime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, String, DateTime, Enum as SQLAlchemyEnum

# Internal library imports
from src.entities.base_entity import BaseEntity, BaseMessage
from src.resources import RoleEnum, EmployeeReturnResource



class EmployeeEntity(BaseEntity):
    __tablename__ = 'employees'
    id: Mapped[str] = Column(String(36), primary_key=True, index=True, nullable=False)
    email: Mapped[str] = Column(String(100), index=True, unique=True, nullable=False)
    hashed_password: Mapped[str] = Column(String(130), nullable=False)
    first_name: Mapped[str] = Column(String(45), nullable=False)
    last_name: Mapped[str] = Column(String(45), nullable=False)
    role: Mapped[RoleEnum] = Column(SQLAlchemyEnum(RoleEnum), nullable=False)
    is_deleted: Mapped[bool] = Column(nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, nullable=False)

    cars = relationship("CarEntity", back_populates="employee")


    def as_resource(self) -> EmployeeReturnResource:
        return EmployeeReturnResource(
            id=self.id,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            role=self.role,
            is_deleted=self.is_deleted,
        )

class EmployeeMesssage(BaseMessage):
    email: str
    hashed_password: str
    first_name: str
    last_name: str
    role: RoleEnum
    is_deleted: bool


