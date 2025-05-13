# External Library imports
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Table, Column, ForeignKey, String, Double, DateTime

# Internal library imports
from src.entities.base_entity import BaseEntity
from src.resources import InsuranceReturnResource


cars_has_insurances = Table(
    'cars_has_insurances',
    BaseEntity.metadata,
    Column('cars_id', String(36), ForeignKey('cars.id'), primary_key=True, nullable=False),
    Column('insurances_id', String(36), ForeignKey('insurances.id'), primary_key=True, nullable=False),
)

class InsuranceEntity(BaseEntity):
    __tablename__ = 'insurances'
    id: Mapped[str] = Column(String(36), primary_key=True, index=True, nullable=False)
    name: Mapped[str] = Column(String(45), unique=True, index=True, nullable=False)
    price: Mapped[float] = Column(Double, nullable=False)
    created_at: Mapped[datetime] = Column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    cars = relationship('CarEntity', secondary=cars_has_insurances, back_populates='insurances')


    def as_resource(self) -> InsuranceReturnResource:
        return InsuranceReturnResource(
            id=self.id,
            name=self.name,
            price=self.price
        )
