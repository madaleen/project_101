"""
Model SQLAlchemy pentru revendicări (claims).

Relația dintre Claim ↔ Donation este 1-la-1: o donație poate fi revendicată
o singură dată. Unicitatea este garantată prin constraint-ul UNIQUE pe donation_id.
"""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Claim(Base):
    """
    Tabelul `claims` – înregistrează revendicările donațiilor.

    Invarianți de integritate:
      - UniqueConstraint(donation_id): O donație nu poate fi revendicată de mai
        mult de un utilizator. Împreună cu tranzacția SQL din router, previne
        race conditions (cazul în care doi utilizatori trimit POST simultan).
    """
    __tablename__ = "claims"
    __table_args__ = (
        UniqueConstraint("donation_id", name="uq_claims_donation"),
    )

    id = Column(Integer, primary_key=True, index=True)

    donation_id = Column(
        Integer,
        ForeignKey("donations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    claimer_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    claimed_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # ── Relații ────────────────────────────────────────────────────────────────
    donation = relationship("Donation", back_populates="claim")
    claimer = relationship("User", back_populates="claims")
