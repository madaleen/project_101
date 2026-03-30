"""
Scheme Pydantic v2 pentru Claims.
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ClaimResponse(BaseModel):
    """DTO de răspuns la revendicarea cu succes a unei donații."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    donation_id: int
    claimer_id: int
    claimed_at: datetime
