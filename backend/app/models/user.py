import enum
from datetime import datetime

from geoalchemy2 import Geography
from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class UserRole(str, enum.Enum):
    Store = "Store"
    NGO = "NGO"
    Volunteer = "Volunteer"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    location: Mapped[Geography | None] = mapped_column(
        Geography(geometry_type="POINT", srid=4326),
        nullable=True,
        comment="Coordonate GPS stocate ca PostGIS Geography(POINT, SRID=4326)",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    donations = relationship("Donation", back_populates="donor", lazy="select")
    claims = relationship("Claim", back_populates="claimer", lazy="select")