# External Library imports
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from sqlalchemy import Column, String, DATETIME, Enum as SQLAlchemyEnum


# Internal library imports
from src.entities.base_entity import BaseEntity
from src.resources import RoleEnum, EmployeeReturnResource


class EmployeeEntity(BaseEntity):
    __tablename__ = 'employees'
    id: Mapped[str] = Column(String(36), primary_key=True, index=True, nullable=False)
    email: Mapped[str] = Column(String(100), index=True, unique=True, nullable=False)
    hashed_password: Mapped[str] = Column(String(130), nullable=False)
    first_name: Mapped[str] = Column(String(45), nullable=False)
    last_name: Mapped[str] = Column(String(45), nullable=False)
    role: Mapped[RoleEnum] = Column(SQLAlchemyEnum(RoleEnum), nullable=False)
    is_deleted: Mapped[bool] = Column(default=False, nullable=False)
    created_at: Mapped[datetime] = Column(DATETIME, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = Column(DATETIME, server_default=func.now(), onupdate=func.now(), nullable=False)


    def as_resource(self) -> EmployeeReturnResource:
        return EmployeeReturnResource(
            id=self.id,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            role=self.role,
            is_deleted=self.is_deleted,
        )