"""
Model SQLAlchemy pentru donații alimentare.

Câmpul `location` (Geography(POINT)) permite interogări spațiale eficiente
cu ST_DWithin în PostgreSQL/PostGIS – mult mai rapid decât a calcula haversine
în Python pentru fiecare rând.
"""
import enum

from geoalchemy2 import Geography
from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class DonationStatus(str, enum.Enum):
    """Ciclul de viață al unei donații."""
    available = "available"  # disponibilă, poate fi revendicată
    claimed = "claimed"      # revendicată de un utilizator
    expired = "expired"      # expirată (nu a mai fost ridicată)


class Donation(Base):
    """
    Tabelul `donations` – stochează ofertele de mâncare ale magazinelor.

    Câmpuri notabile:
      - `location`: PostGIS Geography(POINT) → folosit în query-ul ST_DWithin
        de la endpoint-ul GET /donations/nearby.
      - `status`: gestionat atomic prin tranzacție SQL la endpoint-ul de claiming.
    """
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)

    # ── Donator ────────────────────────────────────────────────────────────────
    donor_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Detalii produs ─────────────────────────────────────────────────────────
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    quantity = Column(Float, nullable=False, default=1.0)          # kg / bucăți
    quantity_unit = Column(String(20), nullable=False, default="kg")
    expiry_time = Column(DateTime(timezone=True), nullable=False)

    # ── Locație PostGIS ────────────────────────────────────────────────────────
    # Stocăm coordonatele donației (nu neapărat sediul magazinului).
    # WKT: 'SRID=4326;POINT(lon lat)' – ex: 'SRID=4326;POINT(26.1025 44.4268)'
    location = Column(
        Geography(geometry_type="POINT", srid=4326),
        nullable=False,
        comment="Coordonate GPS ale donației (PostGIS POINT, SRID 4326)",
    )

    # ── Status ─────────────────────────────────────────────────────────────────
    status = Column(
        Enum(DonationStatus),
        nullable=False,
        default=DonationStatus.available,
        index=True,
    )

    # ── Timestamps ─────────────────────────────────────────────────────────────
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # ── Relații ────────────────────────────────────────────────────────────────
    donor = relationship("User", back_populates="donations")
    claim = relationship("Claim", back_populates="donation", uselist=False)
