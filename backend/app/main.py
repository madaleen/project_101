from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from uuid import UUID
from app.crud import create_location, create_product, find_products_nearby, reserve_product
from app.db import get_db
from app.auth import get_current_user

app = FastAPI()

class DonationCreate(BaseModel):
    name: str
    description: str | None = None
    product_type: str = Field(..., alias="type")
    price: float = 0.0
    quantity: int = 1
    expiry_time: str
    address: str
    lon: float
    lat: float
    radius_km: float = 5.0

    model_config = {"populate_by_name": True}


@app.post("/products")
def create_donation(payload: DonationCreate, db=Depends(get_db), user=Depends(get_current_user)):
    if user.role != "merchant":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only merchants can post donations")

    location = create_location(db, user.id, payload.address, payload.lon, payload.lat)
    if not location:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to create location")

    location_id = location["id"]

    product = create_product(
        db,
        merchant_id=user.id,
        location_id=location_id,
        name=payload.name,
        description=payload.description,
        product_type=payload.product_type,
        price=payload.price,
        quantity=payload.quantity,
        expiry_time=payload.expiry_time
    )
    ngos = find_products_nearby(db, payload.lon, payload.lat, payload.radius_km)
    return {"product": product, "nearby_ngos": ngos}

@app.get("/products/nearby")
def nearby_products(lon: float, lat: float, radius_km: float = 5.0, db=Depends(get_db)):
    return find_products_nearby(db, lon, lat, radius_km)

@app.patch("/products/{product_id}/claim")
def claim_product(product_id: UUID, db=Depends(get_db), user=Depends(get_current_user)):
    product = reserve_product(db, product_id, user.id)
    if not product:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Produsul a fost deja revendicat")
    return product