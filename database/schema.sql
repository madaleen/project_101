-- Initial Schema for Food Saving & Donation Platform

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE user_role AS ENUM ('merchant', 'ngo', 'individual');
CREATE TYPE product_type AS ENUM ('donation', 'discount');
CREATE TYPE product_status AS ENUM ('available', 'claimed', 'sold_out');
CREATE TYPE transaction_status AS ENUM ('reserved', 'picked_up', 'cancelled');

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role user_role NOT NULL,
    firebase_token TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE locations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    address TEXT,
    geom GEOGRAPHY(POINT,4326) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    merchant_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    location_id UUID NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    type product_type NOT NULL,
    price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    quantity INTEGER NOT NULL DEFAULT 1,
    expiry_time TIMESTAMPTZ NOT NULL,
    status product_status NOT NULL DEFAULT 'available',
    image_url TEXT,
    claimed_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    claimer_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    pickup_code VARCHAR(10) UNIQUE NOT NULL,
    status transaction_status NOT NULL DEFAULT 'reserved',
    claimed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    picked_up_at TIMESTAMPTZ,
    receipt_data JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_products_status ON products(status);
CREATE INDEX idx_products_type ON products(type);
CREATE INDEX idx_products_location ON products(location_id);
CREATE INDEX idx_locations_geom ON locations USING GIST(geom);

CREATE OR REPLACE FUNCTION get_entities_within_radius(
    center_lon DOUBLE PRECISION,
    center_lat DOUBLE PRECISION,
    radius_km DOUBLE PRECISION
)
RETURNS TABLE (
    product_id UUID,
    merchant_id UUID,
    location_id UUID,
    name VARCHAR,
    status product_status,
    distance_m DOUBLE PRECISION
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.id,
        p.merchant_id,
        p.location_id,
        p.name,
        p.status,
        ST_Distance(
            l.geom,
            ST_SetSRID(ST_MakePoint(center_lon, center_lat), 4326)::geography
        ) AS distance_m
    FROM products p
    JOIN locations l ON l.id = p.location_id
    WHERE ST_DWithin(
        l.geom,
        ST_SetSRID(ST_MakePoint(center_lon, center_lat), 4326)::geography,
        radius_km * 1000
    )
    AND p.status = 'available'
    ORDER BY distance_m;
END;
$$ LANGUAGE plpgsql STABLE;