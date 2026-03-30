"""
Router pentru donații alimentare.

Endpoint-uri:
  POST /donations/         → creează o donație nouă (doar Store)
  GET  /donations/nearby   → returnează donațiile din raza specificată (ST_DWithin)
"""
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from geoalchemy2.functions import ST_AsText, ST_DWithin, ST_GeogFromText
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, require_role
from app.database import get_db
from app.models.donation import Donation, DonationStatus
from app.models.user import User, UserRole
from app.schemas.donation import DonationCreate, DonationResponse

router = APIRouter(prefix="/donations", tags=["Donații"])


def _wkt_point(lon: float, lat: float) -> str:
    """
    Returnează un WKT Geography Point în formatul așteptat de PostGIS.

    Ordinea corectă PostGIS WKT: POINT(longitudine latitudine).
    Exemplu: POINT(26.1025 44.4268) → București
    """
    return f"SRID=4326;POINT({lon} {lat})"


def _extract_coords(wkt_text: str | None) -> tuple[float | None, float | None]:
    """
    Extrage (lat, lon) dintr-un string WKT de tip 'POINT(lon lat)'.

    PostGIS returnează WKT prin ST_AsText fără prefixul SRID.
    Exemplu input: 'POINT(26.1025 44.4268)' → (44.4268, 26.1025)
    """
    if not wkt_text:
        return None, None
    # Eliminăm 'POINT(' și ')'
    coords_str = wkt_text.replace("POINT(", "").replace(")", "").strip()
    parts = coords_str.split()
    if len(parts) != 2:
        return None, None
    lon, lat = float(parts[0]), float(parts[1])
    return lat, lon


# ── POST /donations/ ───────────────────────────────────────────────────────────

@router.post(
    "/",
    response_model=DonationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Creează o donație nouă (doar Store)",
)
async def create_donation(
    payload: DonationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("Store")),
) -> DonationResponse:
    """
    Creează o donație alimentară.

    - Restricționat la utilizatorii cu rolul **Store**.
    - Coordonatele GPS (lat, lon) sunt convertite în WKT PostGIS.
    - Data de expirare trebuie să fie în viitor.
    """
    donation = Donation(
        donor_id=current_user.id,
        title=payload.title,
        description=payload.description,
        quantity=payload.quantity,
        quantity_unit=payload.quantity_unit,
        expiry_time=payload.expiry_time,
        location=_wkt_point(payload.lon, payload.lat),
        status=DonationStatus.available,
    )
    db.add(donation)
    await db.commit()
    await db.refresh(donation)

    # Construim răspunsul cu coordonatele extrase
    response = DonationResponse.model_validate(donation)
    response.lat = payload.lat
    response.lon = payload.lon
    return response


# ── GET /donations/nearby ──────────────────────────────────────────────────────

@router.get(
    "/nearby",
    response_model=list[DonationResponse],
    summary="Donații disponibile în raza specificată (ST_DWithin)",
)
async def get_nearby_donations(
    lat: float = Query(..., ge=-90.0, le=90.0, description="Latitudinea curentă"),
    lon: float = Query(..., ge=-180.0, le=180.0, description="Longitudinea curentă"),
    radius_km: float = Query(5.0, gt=0, le=500.0, description="Raza de căutare în km"),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),   # orice utilizator autentificat
) -> list[DonationResponse]:
    """
    Returnează donațiile cu status 'available' din raza specificată.

    ## Query Geospațial PostGIS – ST_DWithin

    ```sql
    SELECT d.*, ST_AsText(d.location) AS loc_wkt
    FROM donations d
    WHERE d.status = 'available'
      AND ST_DWithin(
            d.location,                          -- Geography(POINT) al donației
            ST_GeogFromText('SRID=4326;POINT(lon lat)'),  -- punctul curent
            :radius_meters                       -- raza în METRI (nu km!)
          )
    ORDER BY ST_Distance(d.location, ST_GeogFromText(...)) ASC;
    ```

    **De ce ST_DWithin?**
    - Funcționează direct cu tipul `Geography` → distanțele sunt în **metri reali** pe
      suprafața sferică a Pământului (fără distorsionare planară).
    - Folosește automat indexul spațial GIST → performanță O(log N) față de
      calculul brute-force haversine în Python.
    - `radius_km * 1000` convertește în metri, unitatea nativă a Geography.
    """
    radius_m = radius_km * 1000  # ST_DWithin cu Geography lucrează în metri

    # WKT pentru punctul de referință (utilizatorul curent)
    ref_point_wkt = f"SRID=4326;POINT({lon} {lat})"
    ref_point_geo = ST_GeogFromText(ref_point_wkt)

    stmt = (
        select(
            Donation,
            # Extragem WKT din câmpul Geography pentru a reconstitui lat/lon
            ST_AsText(Donation.location).label("loc_wkt"),
        )
        .where(
            Donation.status == DonationStatus.available,
            # ── Interogarea geospațială principală ───────────────────────────
            # ST_DWithin(geog_a, geog_b, raza_m) → True dacă distanța ≤ raza_m
            # Exploatează indexul GIST creat pe coloana `location`.
            ST_DWithin(Donation.location, ref_point_geo, radius_m),
        )
        # Ordonăm după distanță față de utilizator (cel mai apropiat primul)
        .order_by(ST_DWithin(Donation.location, ref_point_geo, radius_m).desc())
    )

    rows = (await db.execute(stmt)).all()

    result: list[DonationResponse] = []
    for donation, loc_wkt in rows:
        resp = DonationResponse.model_validate(donation)
        resp.lat, resp.lon = _extract_coords(loc_wkt)
        result.append(resp)

    return result
