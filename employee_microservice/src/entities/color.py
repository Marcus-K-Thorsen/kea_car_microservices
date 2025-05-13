# External Library imports
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import (
    Table, 
    Column, 
    Integer, 
    String, 
    Double, 
    ForeignKey, 
    DateTime
)

# Internal library imports
from src.resources import ColorReturnResource
from src.entities.base_entity import BaseEntity


models_has_colors = Table(
    'models_has_colors',
    BaseEntity.metadata,
    Column('models_id', String(36), ForeignKey('models.id'), primary_key=True, nullable=False),
    Column('colors_id', String(36), ForeignKey('colors.id'), primary_key=True, nullable=False),
)

class ColorEntity(BaseEntity):
    __tablename__ = 'colors'
    id: Mapped[str] = Column(String(36), primary_key=True, index=True, nullable=False)
    name: Mapped[str] = Column(String(45), unique=True, index=True, nullable=False)
    price: Mapped[float] = Column(Double, nullable=False)
    red_value: Mapped[int] = Column(Integer, nullable=False)
    green_value: Mapped[int] = Column(Integer, nullable=False)
    blue_value: Mapped[int] = Column(Integer, nullable=False)
    created_at: Mapped[datetime] = Column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
    
    models = relationship('ModelEntity', secondary=models_has_colors, back_populates='colors')
    cars = relationship('CarEntity', back_populates='color')


    def as_resource(self) -> ColorReturnResource:
        return ColorReturnResource(
            id=self.id,
            name=self.name,
            price=self.price,
            red_value=self.red_value,
            green_value=self.green_value,
            blue_value=self.blue_value,
        )

