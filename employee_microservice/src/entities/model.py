# External Library imports
from typing import List
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, String, Double, ForeignKey, DateTime


# Internal library imports
from src.entities.brand import BrandEntity
from src.resources import ModelReturnResource
from src.entities.base_entity import BaseEntity
from src.entities.color import ColorEntity, models_has_colors


class ModelEntity(BaseEntity):
    __tablename__ = 'models'
    id: Mapped[str] = Column(String(36), primary_key=True, index=True, nullable=False)
    brands_id: Mapped[str] = Column(String(36), ForeignKey('brands.id'), nullable=False)
    name: Mapped[str] = Column(String(60), unique=True, index=True, nullable=False)
    price: Mapped[float] = Column(Double, nullable=False)
    image_url: Mapped[str] = Column(String(255), nullable=False)
    created_at: Mapped[datetime] = Column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    brand: Mapped[BrandEntity] = relationship('BrandEntity', back_populates='models', lazy=False, uselist=False)
    colors: Mapped[List[ColorEntity]] = relationship('ColorEntity', secondary=models_has_colors, back_populates='models', lazy=False)
    cars = relationship('CarEntity', back_populates='model')

    def as_resource(self) -> ModelReturnResource:
        return ModelReturnResource(
            id=self.id,
            brand=self.brand.as_resource(),
            colors=[color.as_resource() for color in self.colors],
            name=self.name,
            price=self.price,
            image_url=self.image_url,
        )


