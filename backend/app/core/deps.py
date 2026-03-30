"""
Dependențe FastAPI reutilizabile:
  - get_current_user  → orice utilizator autentificat
  - require_role(...)  → factory pentru restricții pe bază de rol
"""
from typing import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.database import get_db
from app.models.user import User

# Schema OAuth2: FastAPI va căuta tokenul în header-ul Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Extrage și validează utilizatorul curent din JWT-ul din header.

    Raises:
        HTTPException 401: Dacă token-ul lipsește, e invalid sau utilizatorul nu există.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Nu s-au putut valida acreditările",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Interogare async pentru utilizator
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user


def require_role(*allowed_roles: str) -> Callable:
    """
    Factory de dependency care restricționează accesul la rolurile specificate.

    Exemplu de utilizare:
        @router.post("/admin-only")
        async def handler(user = Depends(require_role("Store"))):
            ...
    """
    async def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role.value not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Acces interzis. Roluri permise: {', '.join(allowed_roles)}"
                ),
            )
        return current_user

    return role_checker
