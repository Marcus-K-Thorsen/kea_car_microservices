# External Library imports
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import (
    Table, 
    Column, 
    String, 
    Double, 
    ForeignKey, 
    DateTime
)


# Internal library imports
from src.entities.base_entity import BaseEntity
from src.resources import AccessoryReturnResource


cars_has_accessories = Table(
    'cars_has_accessories',
    BaseEntity.metadata,
    Column('cars_id', String(36), ForeignKey('cars.id'), nullable=False, primary_key=True),
    Column('accessories_id', String(36), ForeignKey('accessories.id'), nullable=False, primary_key=True),
)

class AccessoryEntity(BaseEntity):
    __tablename__ = 'accessories'
    id: Mapped[str] = Column(String(36), primary_key=True, index=True, nullable=False)
    name: Mapped[str] = Column(String(60), unique=True, index=True, nullable=False)
    price: Mapped[float] = Column(Double, nullable=False)
    created_at: Mapped[datetime] = Column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    cars = relationship('CarEntity', secondary=cars_has_accessories, back_populates='accessories')


    def as_resource(self) -> AccessoryReturnResource:
        return AccessoryReturnResource(
            id=self.id,
            name=self.name,
            price=self.price
        )


