-- ══════════════════════════════════════════════════════════════════════════════
-- Migrație inițială – Food Waste Combat Platform
-- Cerință: PostgreSQL 14+ cu extensia PostGIS instalată.
-- Rulare: psql -U postgres -d foodsave_db -f migration_001_initial.sql
-- ══════════════════════════════════════════════════════════════════════════════

-- ── 1. Activăm extensia PostGIS ────────────────────────────────────────────────
CREATE EXTENSION IF NOT EXISTS postgis;

-- ── 2. Enum-uri ────────────────────────────────────────────────────────────────
DO $$ BEGIN
    CREATE TYPE user_role AS ENUM ('Store', 'NGO', 'Volunteer');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE donation_status AS ENUM ('available', 'claimed', 'expired');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- ── 3. Tabela users ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id            SERIAL PRIMARY KEY,
    email         VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name     VARCHAR(255) NOT NULL,
    role          user_role    NOT NULL,
    phone         VARCHAR(20),
    -- Geography(POINT, 4326): coordonate GPS în WGS-84
    -- Distanțele calculate de ST_DWithin/ST_Distance sunt în METRI
    location      geography(POINT, 4326),
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- Indexare B-Tree pe email (quick lookup la autentificare)
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- ── 4. Tabela donations ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS donations (
    id            SERIAL PRIMARY KEY,
    donor_id      INTEGER         NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title         VARCHAR(255)    NOT NULL,
    description   TEXT,
    quantity      FLOAT           NOT NULL,
    quantity_unit VARCHAR(20)     NOT NULL DEFAULT 'kg',
    expiry_time   TIMESTAMPTZ     NOT NULL,
    -- Geography(POINT) permite ST_DWithin cu distanțe în metri reali
    location      geography(POINT, 4326) NOT NULL,
    status        donation_status NOT NULL DEFAULT 'available',
    created_at    TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

-- Index spațial GIST pe location – OBLIGATORIU pentru performanță ST_DWithin
-- Fără acest index, ST_DWithin face full table scan (O(N))
-- Cu GIST, interogarea devine O(log N)
CREATE INDEX IF NOT EXISTS idx_donations_location_gist
    ON donations USING GIST (location);

-- Index B-Tree pe status – filtrare rapidă pe 'available'
CREATE INDEX IF NOT EXISTS idx_donations_status ON donations(status);

-- ── 5. Tabela claims ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS claims (
    id           SERIAL PRIMARY KEY,
    donation_id  INTEGER NOT NULL REFERENCES donations(id) ON DELETE CASCADE,
    claimer_id   INTEGER NOT NULL REFERENCES users(id)    ON DELETE CASCADE,
    claimed_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    -- UNIQUE garantat la nivel DB: o donație → un singur claim
    CONSTRAINT uq_claims_donation UNIQUE (donation_id)
);

CREATE INDEX IF NOT EXISTS idx_claims_donation_id ON claims(donation_id);
CREATE INDEX IF NOT EXISTS idx_claims_claimer_id  ON claims(claimer_id);

-- ══════════════════════════════════════════════════════════════════════════════
-- Exemplu de query geospațial ST_DWithin
-- Găsește donațiile disponibile în raza de 5 km față de București (centru)
-- ══════════════════════════════════════════════════════════════════════════════
/*
SELECT
    d.id,
    d.title,
    d.quantity,
    d.quantity_unit,
    d.expiry_time,
    d.status,
    -- Distanța în km față de punctul de referință
    ROUND(
        (ST_Distance(
            d.location,
            ST_GeogFromText('SRID=4326;POINT(26.1025 44.4268)')
        ) / 1000)::numeric,
        2
    ) AS distance_km,
    -- Coordonate WKT pentru deserialization în Python
    ST_AsText(d.location) AS location_wkt
FROM donations d
WHERE
    d.status = 'available'
    AND ST_DWithin(
        d.location,
        ST_GeogFromText('SRID=4326;POINT(26.1025 44.4268)'),
        5000  -- 5 km în metri (Geography lucrează în metri)
    )
ORDER BY distance_km ASC;
*/
