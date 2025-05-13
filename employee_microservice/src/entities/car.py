# External Library imports
from typing import List
from sqlalchemy.sql import func
from datetime import date, datetime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import (
    Column, 
    String, 
    Double, 
    Date, 
    ForeignKey, 
    DateTime
)


# Internal library imports
from src.entities.model import ModelEntity
from src.entities.color import ColorEntity
from src.resources import CarReturnResource
from src.entities.base_entity import BaseEntity
from src.entities.customer import CustomerEntity
from src.entities.employee import EmployeeEntity
from src.entities.accessory import AccessoryEntity, cars_has_accessories
from src.entities.insurance import InsuranceEntity, cars_has_insurances




class CarEntity(BaseEntity):
    __tablename__ = 'cars'
    id: Mapped[str] = Column(String(36), primary_key=True, index=True, nullable=False)
    models_id: Mapped[str] = Column(String(36), ForeignKey('models.id'), nullable=False)
    colors_id: Mapped[str] = Column(String(36), ForeignKey('colors.id'), nullable=False)
    customers_id: Mapped[str] = Column(String(36), ForeignKey('customers.id'), nullable=False)
    employees_id: Mapped[str] = Column(String(36), ForeignKey('employees.id'), nullable=False)
    total_price: Mapped[float] = Column(Double, nullable=False)
    purchase_deadline: Mapped[date] = Column(Date, nullable=False)
    created_at: Mapped[datetime] = Column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    purchase = relationship("PurchaseEntity", back_populates="car", uselist=False)
    model: Mapped[ModelEntity] = relationship("ModelEntity", back_populates="cars", lazy=False)
    color: Mapped[ColorEntity] = relationship("ColorEntity", back_populates="cars", lazy=False)
    customer: Mapped[CustomerEntity] = relationship("CustomerEntity", back_populates="cars", lazy=False)
    employee: Mapped[EmployeeEntity] = relationship("EmployeeEntity", back_populates="cars", lazy=False)
    accessories: Mapped[List[AccessoryEntity]] = relationship(
        "AccessoryEntity", secondary=cars_has_accessories, back_populates="cars", lazy=False
    )
    insurances: Mapped[List[InsuranceEntity]] = relationship(
        "InsuranceEntity", secondary=cars_has_insurances, back_populates="cars", lazy=False
    )

    def as_resource(self, is_purchased: bool) -> CarReturnResource:
        if not isinstance(is_purchased, bool):
            raise TypeError(f"is_purchased must be of type bool, "
                            f"not {type(is_purchased).__name__}.")
        return CarReturnResource(
            id=self.id,
            total_price=self.total_price,
            purchase_deadline=self.purchase_deadline,
            model=self.model.as_resource(),
            color=self.color.as_resource(),
            customer=self.customer.as_resource(),
            employee=self.employee.as_resource(),
            accessories=[accessory.as_resource() for accessory in self.accessories],
            insurances=[insurance.as_resource() for insurance in self.insurances],
            is_purchased=is_purchased,
        )
