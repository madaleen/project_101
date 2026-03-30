"""
Router pentru autentificare: înregistrare și login.

Endpoint-uri:
  POST /auth/register  → creează un cont nou
  POST /auth/login     → returnează un JWT Bearer token
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, get_password_hash, verify_password
from app.database import get_db
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["Autentificare"])


def _coords_to_wkt(lat: float, lon: float) -> str:
    """Convertește lat/lon în WKT Geography Point (PostGIS)."""
    # PostGIS WKT: POINT(lon lat) – atenție: ordinea este lon, lat!
    return f"SRID=4326;POINT({lon} {lat})"


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Înregistrează un cont nou",
)
async def register(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Creează un utilizator nou în platformă.

    - Verifică unicitatea email-ului.
    - Hash-uiește parola cu bcrypt.
    - Dacă lat/lon sunt furnizate, converteşte în WKT PostGIS.
    """
    # Verificare email duplicat
    result = await db.execute(select(User).where(User.email == payload.email))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Adresa de email este deja înregistrată.",
        )

    location_wkt = None
    if payload.lat is not None and payload.lon is not None:
        location_wkt = _coords_to_wkt(payload.lat, payload.lon)

    user = User(
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        full_name=payload.full_name,
        role=payload.role,
        phone=payload.phone,
        location=location_wkt,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post(
    "/login",
    response_model=Token,
    summary="Autentifică-te și obține un JWT",
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> Token:
    """
    Autentifică utilizatorul folosind OAuth2 Password Flow.

    Trimite `username` (email) și `password` ca form-data.
    Returnează un JWT Bearer token valid 24 de ore.
    """
    result = await db.execute(
        select(User).where(User.email == form_data.username)
    )
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email sau parolă incorectă.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(subject=user.email, role=user.role.value)
    return Token(access_token=token)
