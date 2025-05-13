# External Library imports
from sqlalchemy.sql import func
from datetime import date, datetime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, String, Date, ForeignKey, DateTime


# Internal library imports
from src.entities.car import CarEntity
from src.entities.base_entity import BaseEntity
from src.resources import PurchaseReturnResource


class PurchaseEntity(BaseEntity):
    __tablename__ = 'purchases'
    id: Mapped[str] = Column(String(36), primary_key=True, index=True, nullable=False)
    cars_id: Mapped[str] = Column(String(36), ForeignKey('cars.id'), nullable=False)
    date_of_purchase: Mapped[date] = Column(Date, nullable=False)
    created_at: Mapped[datetime] = Column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    car: Mapped[CarEntity] = relationship('CarEntity', back_populates='purchase', uselist=False, lazy=False)


    def as_resource(self) -> PurchaseReturnResource:
        return PurchaseReturnResource(
            id=self.id,
            date_of_purchase=self.date_of_purchase,
            car=self.car.as_resource(is_purchased=True),
        )

