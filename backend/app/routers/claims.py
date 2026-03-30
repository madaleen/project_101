"""
Router pentru revendicarea donațiilor (Claims).

Endpoint-uri:
  POST /claims/{donation_id}  → revendică o donație (NGO sau Volunteer)

## Prevenirea rezervărilor duble (race condition)

Problemă: Doi utilizatori trimit POST /claims/{id} simultan.
Fără protecție → ambele tranzacții citesc status='available' și ambele
scriu status='claimed', rezultând în două înregistrări de claim.

Soluție implementată (dublă protecție):
  1. **SELECT ... FOR UPDATE** (row-level lock):
     Prima tranzacție care ajunge la SELECT blochează rândul.
     A doua tranzacție așteaptă blocarea să fie eliberată, după care
     recitește rândul și vede status='claimed' → aruncă 409.
  2. **UniqueConstraint(donation_id)** pe tabela `claims`:
     Al doilea INSERT (dacă ar ajunge cumva) eșuează la nivel de bază de date.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, require_role
from app.database import get_db
from app.models.claim import Claim
from app.models.donation import Donation, DonationStatus
from app.models.user import User
from app.schemas.claim import ClaimResponse

router = APIRouter(prefix="/claims", tags=["Revendicări"])


@router.post(
    "/{donation_id}",
    response_model=ClaimResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Revendică o donație disponibilă (NGO sau Volunteer)",
)
async def claim_donation(
    donation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("NGO", "Volunteer")),
) -> ClaimResponse:
    """
    Revendică o donație cu status 'available', schimbând statusul în 'claimed'.

    ## Flux tranzacțional

    ```
    BEGIN TRANSACTION
      SELECT * FROM donations WHERE id = :id FOR UPDATE   ← lock exclusiv pe rând
      ─── verificare status ────────────────────────────────────────────────────
      UPDATE donations SET status = 'claimed' WHERE id = :id
      INSERT INTO claims (donation_id, claimer_id) VALUES (:id, :user_id)
    COMMIT  (sau ROLLBACK la eroare)
    ```

    **SELECT FOR UPDATE** garantează că un singur fir de execuție poate
    modifica simultan același rând. Orice altă tranzacție concurentă va
    aștepta eliberarea lock-ului, reciti statusul ('claimed') și va
    returna 409 Conflict.
    """
    try:
        # ── 1. Pornim tranzacția (sesiunea async este deja în tranzacție) ──────
        # ── 2. Blocăm rândul donației cu SELECT FOR UPDATE ────────────────────
        result = await db.execute(
            select(Donation)
            .where(Donation.id == donation_id)
            .with_for_update()       # ← cheie: lock exclusiv la nivel de rând
        )
        donation = result.scalars().first()

        # ── 3. Validări ───────────────────────────────────────────────────────
        if donation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Donația cu id={donation_id} nu a fost găsită.",
            )

        if donation.status != DonationStatus.available:
            # Status deja modificat de o altă tranzacție concurentă
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Donația nu mai este disponibilă "
                    f"(status curent: {donation.status.value})."
                ),
            )

        if donation.donor_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nu poți revendica propria donație.",
            )

        # ── 4. Schimbăm statusul donației ─────────────────────────────────────
        donation.status = DonationStatus.claimed

        # ── 5. Creăm înregistrarea de claim ───────────────────────────────────
        claim = Claim(
            donation_id=donation_id,
            claimer_id=current_user.id,
        )
        db.add(claim)

        # ── 6. Commit atomic (ambele operații sau niciuna) ─────────────────────
        await db.commit()
        await db.refresh(claim)

    except IntegrityError:
        # UniqueConstraint(donation_id) declanșat de o tranzacție paralelă
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Donația a fost deja revendicată de altcineva.",
        )

    return claim
