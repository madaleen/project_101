"""
Motor asincron SQLAlchemy 2.0-style cu suport PostGIS.

Folosim asyncpg drept driver și GeoAlchemy2 pentru tipul Geography(POINT).
"""
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# ── Motor async ────────────────────────────────────────────────────────────────
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,       # loghează SQL-ul în modul DEBUG
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,        # verifică conexiunile înainte de a le reutiliza
)

# ── Factory sesiune ────────────────────────────────────────────────────────────
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,    # obiectele nu expiră după commit (util cu async)
)


# ── Clasă de bază pentru modele ────────────────────────────────────────────────
class Base(DeclarativeBase):
    """Clasă de bază din care moștenesc TOATE modelele SQLAlchemy."""
    pass


# ── Dependency FastAPI ─────────────────────────────────────────────────────────
async def get_db() -> AsyncSession:  # type: ignore[misc]
    """
    Generator de sesiune async utilizat ca dependency în FastAPI.

    Exemplu de utilizare:
        @router.get("/resource")
        async def handler(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        yield session
