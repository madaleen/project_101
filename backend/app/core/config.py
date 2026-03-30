"""
Configurare centralizată a aplicației folosind pydantic-settings.
Toate valorile sunt citite din variabilele de mediu / fișierul .env.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    # ── Aplicație ─────────────────────────────────────────────────────────────
    APP_NAME: str = "Food Waste Combat Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # ── Bază de date (asyncpg + PostGIS) ─────────────────────────────────────
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:password@localhost:5432/foodsave_db"
    )

    # ── JWT ───────────────────────────────────────────────────────────────────
    SECRET_KEY: str = "SCHIMBA_ACEASTA_CHEIE_IN_PRODUCTIE"  # min 32 chars
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 ore

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


@lru_cache()
def get_settings() -> Settings:
    """Returnează o instanță singleton a setărilor (cache LRU)."""
    return Settings()


settings = get_settings()
