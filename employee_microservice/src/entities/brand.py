# External Library imports
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import Mapped, relationship

# Internal library imports
from src.entities.base_entity import BaseEntity
from src.resources.brand_resource import BrandReturnResource


class BrandEntity(BaseEntity):
    __tablename__ = 'brands'
    id: Mapped[str] = Column(String(36), primary_key=True, index=True, nullable=False)
    name: Mapped[str] = Column(String(60), unique=True, index=True, nullable=False)
    logo_url: Mapped[str] = Column(String(255), nullable=False)
    created_at: Mapped[datetime] = Column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
    models = relationship('ModelEntity', back_populates='brand')


    def as_resource(self) -> BrandReturnResource:
        return BrandReturnResource(
            id=self.id,
            name=self.name,
            logo_url=self.logo_url,
        )

