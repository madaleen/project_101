"""
Model SQLAlchemy pentru utilizator.

Câmpul `location` folosește tipul Geography(POINT, 4326) din extensia PostGIS,
care stochează coordonatele GPS folosind sistemul de referință WGS-84 (SRID 4326).
Avantajul față de Float lat/lng: calculele de distanță (ST_DWithin, ST_Distance)
operează direct în metri / km, fără aproximări sferice manuale.
"""
import enum

from geoalchemy2 import Geography  # pachet: geoalchemy2
from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class UserRole(str, enum.Enum):
    """Rolurile suportate în platformă."""
    Store = "Store"          # Magazin / Restaurante – poate crea donații
    NGO = "NGO"              # Organizație non-profit – poate revendica în bulk
    Volunteer = "Volunteer"  # Voluntar individual – poate revendica singular


class User(Base):
    """
    Tabelul `users` – stochează conturile din platformă.

    Câmpuri notabile:
      - `location`: tip PostGIS Geography(POINT) → stocare eficientă a coordonatelor GPS.
        Exemplu de valoare WKT: 'SRID=4326;POINT(26.1025 44.4268)' (lon, lat București).
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    phone = Column(String(20), nullable=True)

    # ── Locație PostGIS ────────────────────────────────────────────────────────
    # Geography vs Geometry: Geography ține cont de curbura Pământului → distanțe
    # exacte în metri chiar și pe distanțe mari. SRID 4326 = WGS-84 (lat/lon GPS).
    location = Column(
        Geography(geometry_type="POINT", srid=4326),
        nullable=True,
        comment="Coordonate GPS stocate ca PostGIS Geography(POINT, SRID=4326)",
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # ── Relații ────────────────────────────────────────────────────────────────
    donations = relationship("Donation", back_populates="donor", lazy="select")
    claims = relationship("Claim", back_populates="claimer", lazy="select")
