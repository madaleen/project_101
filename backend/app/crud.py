from sqlalchemy import text

def _row_to_dict(row):
    if row is None:
        return None
    if hasattr(row, "_mapping"):
        return dict(row._mapping)
    return dict(row)

def create_location(db, user_id, address, lon, lat):
    sql = text("""
        INSERT INTO locations (user_id, address, geom, created_at, updated_at)
        VALUES (
            :user_id,
            :address,
            ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography,
            now(),
            now()
        )
        RETURNING id, user_id, address, geom, created_at, updated_at
    """)
    result = db.execute(sql, {
        "user_id": str(user_id),
        "address": address,
        "lon": lon,
        "lat": lat,
    })
    row = result.fetchone()
    db.commit()
    return _row_to_dict(row)

def create_product(db, merchant_id, location_id, name, description, product_type, price, quantity, expiry_time):
    sql = text("""
        INSERT INTO products (
            merchant_id,
            location_id,
            name,
            description,
            "type",
            price,
            quantity,
            expiry_time,
            status,
            created_at,
            updated_at
        ) VALUES (
            :merchant_id,
            :location_id,
            :name,
            :description,
            :product_type,
            :price,
            :quantity,
            :expiry_time,
            'available',
            now(),
            now()
        )
        RETURNING *
    """)
    result = db.execute(sql, {
        "merchant_id": str(merchant_id),
        "location_id": str(location_id),
        "name": name,
        "description": description,
        "product_type": product_type,
        "price": price,
        "quantity": quantity,
        "expiry_time": expiry_time,
    })
    row = result.fetchone()
    db.commit()
    return _row_to_dict(row)

def find_products_nearby(db, lon, lat, radius_km):
    sql = text("""
        SELECT p.*,
               ST_Distance(l.geom, center.pt) AS distance_m
        FROM products p
        JOIN locations l ON l.id = p.location_id,
             (SELECT ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography AS pt) AS center
        WHERE ST_DWithin(l.geom, center.pt, :radius_m)
          AND p.status = 'available'
        ORDER BY distance_m
    """)
    result = db.execute(sql, {
        "lon": lon,
        "lat": lat,
        "radius_m": radius_km * 1000,
    })
    return [_row_to_dict(row) for row in result.fetchall()]

def reserve_product(db, product_id, claimer_id):
    sql = text("""
        UPDATE products
        SET status = 'claimed',
            claimed_by = :claimer_id,
            updated_at = now()
        WHERE id = :product_id
          AND status = 'available'
        RETURNING *
    """)
    result = db.execute(sql, {
        "product_id": str(product_id),
        "claimer_id": str(claimer_id),
    })
    row = result.fetchone()
    if row is None:
        return None
    db.commit()
    return _row_to_dict(row)