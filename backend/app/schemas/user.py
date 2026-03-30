"""
Scheme Pydantic v2 pentru User și Token.

Notă Pydantic v2:
  - Înlocuim `class Config: orm_mode = True` cu `model_config = ConfigDict(from_attributes=True)`.
  - Folosim `model_validator` și `field_validator` în loc de @validator.
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from app.models.user import UserRole


# ── Token ──────────────────────────────────────────────────────────────────────

class Token(BaseModel):
    """Răspuns la autentificarea cu succes."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Payload extras din JWT (intern)."""
    email: str | None = None
    role: str | None = None


# ── User ───────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    """
    Date cerute la înregistrare.

    Coordonatele GPS (lat / lon) sunt opționale la creare, dar recomandate
    pentru a putea găsi donații în proximitate.
    """
    email: EmailStr
    password: str = Field(min_length=8, description="Minim 8 caractere")
    full_name: str = Field(min_length=2, max_length=255)
    role: UserRole
    phone: str | None = None
    lat: float | None = Field(None, ge=-90.0, le=90.0)
    lon: float | None = Field(None, ge=-180.0, le=180.0)

    @model_validator(mode="after")
    def coords_both_or_neither(self) -> "UserCreate":
        """lat și lon trebuie furnizate împreună sau deloc."""
        if (self.lat is None) != (self.lon is None):
            raise ValueError("Furnizați atât 'lat' cât și 'lon', sau niciunul.")
        return self


class UserLogin(BaseModel):
    """Date cerute la autentificare (OAuth2 password flow)."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """DTO de răspuns – nu expune parola sau hash-ul."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    phone: str | None
    created_at: datetime
