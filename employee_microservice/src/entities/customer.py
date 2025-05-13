# External Library imports
from typing import Optional
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import Mapped, relationship

# Internal library imports
from src.entities.base_entity import BaseEntity
from src.resources import CustomerReturnResource


class CustomerEntity(BaseEntity):
    __tablename__ = 'customers'
    id: Mapped[str] = Column(String(36), primary_key=True, index=True, nullable=False)
    email: Mapped[str] = Column(String(50), unique=True, index=True, nullable=False)
    phone_number: Mapped[Optional[str]] = Column(String(30), nullable=True)
    first_name: Mapped[str] = Column(String(45), nullable=False)
    last_name: Mapped[str] = Column(String(45), nullable=False)
    address: Mapped[Optional[str]] = Column(String(255), nullable=True)
    created_at: Mapped[datetime] = Column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    cars = relationship('CarEntity', back_populates='customer')


    def as_resource(self) -> CustomerReturnResource:
        return CustomerReturnResource(
            id=self.id,
            email=self.email,
            phone_number=self.phone_number,
            first_name=self.first_name,
            last_name=self.last_name,
            address=self.address,
        )

