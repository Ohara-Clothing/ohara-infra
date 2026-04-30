import uuid
from sqlalchemy import ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base

class FitClothesEntity(Base):
    __tablename__ = "fit_clothes"
    __table_args__ = (
        UniqueConstraint("fitId", "clothesId", name="uq_fit_clothes_fitId_clothesId"),
    )

    fitClothesId: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()")
    )
    fitId: Mapped[uuid.UUID] = mapped_column(ForeignKey("fits.fitId"))
    clothesId: Mapped[uuid.UUID] = mapped_column(ForeignKey("clothes.clothesId"))

    fit = relationship("FitEntity", back_populates="fit_clothes")
    clothes = relationship("ClothesEntity", back_populates="fit_clothes")
