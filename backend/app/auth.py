from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

class User(BaseModel):
    id: str
    role: str
    email: str

def get_current_user():
    # placeholder pentru testare
    return User(
        id="00000000-0000-0000-0000-000000000000",
        role="merchant",
        email="merchant@example.com",
    )