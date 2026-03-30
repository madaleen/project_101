"""
Punctul de intrare al aplicației FastAPI.

Structura modulară:
  app/
  ├── core/
  │   ├── config.py    – setări pydantic-settings
  │   ├── security.py  – bcrypt + JWT
  │   └── deps.py      – dependențe FastAPI (get_current_user, require_role)
  ├── models/
  │   ├── user.py      – User cu Geography(POINT) PostGIS
  │   ├── donation.py  – Donation cu status enum
  │   └── claim.py     – Claim cu UniqueConstraint
  ├── schemas/
  │   ├── user.py      – Pydantic v2 UserCreate, UserResponse, Token
  │   ├── donation.py  – DonationCreate, DonationResponse, NearbyQueryParams
  │   └── claim.py     – ClaimResponse
  ├── routers/
  │   ├── auth.py      – POST /auth/register, POST /auth/login
  │   ├── donations.py – POST /donations/, GET /donations/nearby (ST_DWithin)
  │   └── claims.py    – POST /claims/{donation_id} (SELECT FOR UPDATE)
  └── database.py      – motor async SQLAlchemy 2.0 + get_db dependency
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database import Base, engine
from app.routers import auth, claims, donations


# ── Lifespan: creare tabele la pornire (dezvoltare) ───────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Gestionează evenimentele de startup / shutdown ale aplicației.

    La startup: creăm tabelele dacă nu există (util în dev).
    În producție, folosiți Alembic pentru migrații!
    """
    # Importăm modelele pentru ca metadata-ul să fie populat
    import app.models.claim      # noqa: F401 – înregistrează Claim în Base.metadata
    import app.models.donation   # noqa: F401 – înregistrează Donation în Base.metadata
    import app.models.user       # noqa: F401 – înregistrează User în Base.metadata

    async with engine.begin() as conn:
        # ATENȚIE: Nu folosiți create_all în producție! Folosiți Alembic.
        await conn.run_sync(Base.metadata.create_all)

    yield  # aplicația rulează

    # Shutdown: închidem conexiunile
    await engine.dispose()


# ── Instanța FastAPI ───────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "API asincron pentru platforma de combatere a risipei alimentare.\n\n"
        "## Roluri\n"
        "- **Store** – Poate crea donații alimentare.\n"
        "- **NGO** – Poate revendica donații în bulk pentru organizație.\n"
        "- **Volunteer** – Poate revendica donații individual.\n\n"
        "## Autentificare\n"
        "Folosim OAuth2 Password Flow cu JWT Bearer token. "
        "Click pe **Authorize** și introdu email + parolă."
    ),
    lifespan=lifespan,
)

# ── CORS ───────────────────────────────────────────────────────────────────────
# Ajustați `allow_origins` în producție pentru a permite doar domeniile voastre!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routere ────────────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(donations.router)
app.include_router(claims.router)


# ── Health check ───────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"], summary="Verificare stare API")
async def root() -> dict:
    return {
        "status": "online",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }
