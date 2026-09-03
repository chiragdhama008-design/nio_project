-- UrbanShield AI — PostgreSQL Schema
-- Run this against your Supabase PostgreSQL database.

CREATE TABLE IF NOT EXISTS zones (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    type        TEXT NOT NULL,
    description TEXT,
    lat         DOUBLE PRECISION,
    lng         DOUBLE PRECISION,
    risk_level  TEXT DEFAULT 'normal',
    status      TEXT DEFAULT 'active',
    created_at  TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS sensors (
    id          TEXT PRIMARY KEY,
    zone_id     TEXT NOT NULL REFERENCES zones(id),
    type        TEXT NOT NULL,
    unit        TEXT NOT NULL,
    label       TEXT,
    status      TEXT DEFAULT 'online',
    lat         DOUBLE PRECISION,
    lng         DOUBLE PRECISION,
    created_at  TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS sensor_readings (
    id          BIGSERIAL PRIMARY KEY,
    sensor_id   TEXT NOT NULL REFERENCES sensors(id),
    zone_id     TEXT NOT NULL REFERENCES zones(id),
    type        TEXT NOT NULL,
    value       DOUBLE PRECISION NOT NULL,
    unit        TEXT,
    timestamp   TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_readings_zone_time ON sensor_readings(zone_id, timestamp DESC);
CREATE INDEX idx_readings_sensor_time ON sensor_readings(sensor_id, timestamp DESC);

CREATE TABLE IF NOT EXISTS incidents (
    id                  TEXT PRIMARY KEY,
    type                TEXT NOT NULL,
    zone_id             TEXT NOT NULL REFERENCES zones(id),
    severity            TEXT NOT NULL,
    confidence          DOUBLE PRECISION,
    risk_score          DOUBLE PRECISION,
    status              TEXT DEFAULT 'active',
    detected_conditions JSONB,
    recommended_actions JSONB,
    created_at          TIMESTAMPTZ DEFAULT now(),
    resolved_at         TIMESTAMPTZ
);

CREATE INDEX idx_incidents_zone ON incidents(zone_id);
CREATE INDEX idx_incidents_status ON incidents(status);

CREATE TABLE IF NOT EXISTS recommended_actions (
    id          BIGSERIAL PRIMARY KEY,
    incident_id TEXT REFERENCES incidents(id),
    action      TEXT NOT NULL,
    priority    INTEGER DEFAULT 0,
    status      TEXT DEFAULT 'pending',
    created_at  TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS simulation_events (
    id          BIGSERIAL PRIMARY KEY,
    type        TEXT NOT NULL,
    status      TEXT DEFAULT 'running',
    parameters  JSONB,
    started_at  TIMESTAMPTZ DEFAULT now(),
    ended_at    TIMESTAMPTZ
);
