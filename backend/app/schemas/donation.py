"""
Scheme Pydantic v2 pentru Donații.

Coordonatele GPS (lat / lon) sunt furnizate de client la creare
și convertite în WKT GeoJSON înainte de a fi trimise la PostGIS.
Răspunsul include coordonatele extrapolate înapoi din câmpul Geography.
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.donation import DonationStatus


class DonationCreate(BaseModel):
    """
    Payload primit la POST /donations/.

    Exemplu:
        {
          "title": "Sandvișuri integrale",
          "description": "Nedesfăcute, data de azi",
          "quantity": 15,
          "quantity_unit": "buc",
          "expiry_time": "2026-03-30T22:00:00+03:00",
          "lat": 44.4268,
          "lon": 26.1025
        }
    """
    title: str = Field(min_length=3, max_length=255)
    description: str | None = Field(None, max_length=1000)
    quantity: float = Field(gt=0, description="Cantitate (trebuie să fie pozitivă)")
    quantity_unit: str = Field(default="kg", max_length=20)
    expiry_time: datetime
    lat: float = Field(ge=-90.0, le=90.0, description="Latitudine WGS-84")
    lon: float = Field(ge=-180.0, le=180.0, description="Longitudine WGS-84")


class DonationResponse(BaseModel):
    """
    DTO de răspuns pentru o donație.

    `lat` și `lon` sunt populate de router din câmpul Geography stocat.
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    donor_id: int
    title: str
    description: str | None
    quantity: float
    quantity_unit: str
    expiry_time: datetime
    status: DonationStatus
    created_at: datetime
    # Coordonate GPS extrase din Geography(POINT) de către router
    lat: float | None = None
    lon: float | None = None


class NearbyQueryParams(BaseModel):
    """Parametri de interogare pentru GET /donations/nearby."""
    lat: float = Field(ge=-90.0, le=90.0)
    lon: float = Field(ge=-180.0, le=180.0)
    radius_km: float = Field(default=5.0, gt=0, le=500.0)
