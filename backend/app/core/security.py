"""
Utilități pentru securitate:
  - hashing parole (bcrypt via passlib)
  - creare / decodare token JWT (python-jose)
"""
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Context bcrypt pentru hashing parole
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ── Parole ─────────────────────────────────────────────────────────────────────

def get_password_hash(password: str) -> str:
    """Returnează hash-ul bcrypt al parolei în clar."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifică dacă parola în clar corespunde hash-ului stocat."""
    return pwd_context.verify(plain_password, hashed_password)


# ── JWT ────────────────────────────────────────────────────────────────────────

def create_access_token(
    subject: str,
    role: str,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Creează un JWT Bearer token.

    Args:
        subject: De obicei email-ul utilizatorului (câmpul 'sub').
        role: Rolul utilizatorului (Store | NGO | Volunteer).
        expires_delta: Durată personalizată de expirare. Dacă None,
                       se folosește ACCESS_TOKEN_EXPIRE_MINUTES din settings.

    Returns:
        Token JWT semnat ca string.
    """
    expire = datetime.now(timezone.utc) + (
        expires_delta
        or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload: dict[str, Any] = {
        "sub": subject,
        "role": role,
        "exp": expire,
        "iat": datetime.now(timezone.utc),  # issued-at
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decodează și validează un JWT Bearer token.

    Raises:
        JWTError: Dacă token-ul este invalid sau expirat.
    """
    return jwt.decode(  # type: ignore[return-value]
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )
