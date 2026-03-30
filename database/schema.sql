-- Initial Schema for Food Saving & Donation Platform

-- Enable PostGIS for geolocation features
CREATE EXTENSION IF NOT EXISTS postgis;

-- Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('merchant', 'ngo', 'individual')),
    location GEOGRAPHY(POINT), -- Lat/Lng for proximity calculations
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products/Donations Table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    merchant_id INTEGER REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    type VARCHAR(50) NOT NULL CHECK (type IN ('donation', 'discount')),
    price DECIMAL(10, 2) DEFAULT 0.00, -- 0 for donations
    quantity INTEGER NOT NULL DEFAULT 1,
    expiry_time TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'available' CHECK (status IN ('available', 'claimed', 'sold_out')),
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transactions Table (Traceability)
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    claimer_id INTEGER REFERENCES users(id),
    pickup_code VARCHAR(10) UNIQUE NOT NULL, -- QR code representation
    status VARCHAR(50) NOT NULL DEFAULT 'reserved' CHECK (status IN ('reserved', 'picked_up', 'cancelled')),
    claimed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    picked_up_at TIMESTAMP
);

-- Indices for performance
CREATE INDEX idx_products_status ON products(status);
CREATE INDEX idx_products_type ON products(type);
CREATE INDEX idx_users_role ON users(role);
-- Spatial index for geolocation
CREATE INDEX idx_users_location ON users USING GIST(location);
