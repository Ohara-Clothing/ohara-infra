import uuid
from decimal import Decimal
from sqlalchemy import String, Numeric, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class ClothesEntity(Base):
    __tablename__ = "clothes"

    clothesId: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()")
    )
    userId: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.userId"))
    clothesType: Mapped[str] = mapped_column(String, nullable=True)
    color: Mapped[str] = mapped_column(String, nullable=True)
    size: Mapped[str] = mapped_column(String, nullable=True)
    brand: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=True)
    imageKey: Mapped[str] = mapped_column(String, nullable=True)

    user = relationship("UserEntity", back_populates="clothes")
    fit_clothes = relationship(
        "FitClothesEntity", back_populates="clothes", cascade="all, delete-orphan"
    )
