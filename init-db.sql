-- BRAINBLUE URBAIN - Database Initialization Script
-- PostGIS + PostgreSQL Setup

-- Créer extensions
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
CREATE EXTENSION IF NOT EXISTS postgis_raster;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS uuid-ossp;

-- Créer schémas
CREATE SCHEMA IF NOT EXISTS public;
CREATE SCHEMA IF NOT EXISTS spatial;
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS logging;

-- Créer type pour status
CREATE TYPE network_status AS ENUM (
    'operational',
    'maintenance',
    'warning',
    'critical',
    'offline'
);

CREATE TYPE risk_level AS ENUM (
    'low',
    'medium',
    'high',
    'critical'
);

CREATE TYPE anomaly_type AS ENUM (
    'leak',
    'pressure_drop',
    'contamination',
    'burst',
    'high_flow',
    'low_flow'
);

-- Créer tables avec PostGIS

CREATE TABLE spatial.water_networks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    city VARCHAR(50) NOT NULL,
    network_type VARCHAR(30) NOT NULL,
    geometry GEOMETRY(POINT, 4326),
    capacity FLOAT,
    current_flow FLOAT,
    pressure FLOAT,
    status network_status DEFAULT 'operational',
    age_years INTEGER,
    last_maintenance TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_geometry CHECK (ST_IsValid(geometry))
);

CREATE TABLE spatial.risk_zones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    city VARCHAR(50) NOT NULL,
    risk_type VARCHAR(30) NOT NULL,
    geometry GEOMETRY(POLYGON, 4326),
    risk_level risk_level DEFAULT 'medium',
    probability FLOAT,
    affected_population INTEGER,
    detected_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    predicted_date TIMESTAMP,
    resolved_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_geometry CHECK (ST_IsValid(geometry))
);

CREATE TABLE spatial.water_paths (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    city VARCHAR(50) NOT NULL,
    path_type VARCHAR(30) NOT NULL,
    geometry GEOMETRY(LINESTRING, 4326),
    width FLOAT,
    quality VARCHAR(20),
    flow_rate VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_geometry CHECK (ST_IsValid(geometry))
);

-- Indices spatiales pour performance
CREATE INDEX idx_water_networks_geom ON spatial.water_networks USING GIST (geometry);
CREATE INDEX idx_risk_zones_geom ON spatial.risk_zones USING GIST (geometry);
CREATE INDEX idx_water_paths_geom ON spatial.water_paths USING GIST (geometry);
CREATE INDEX idx_water_networks_city ON spatial.water_networks(city);
CREATE INDEX idx_risk_zones_city ON spatial.risk_zones(city);
CREATE INDEX idx_water_paths_city ON spatial.water_paths(city);

-- Insérer données de démonstration Dakar

INSERT INTO spatial.water_networks (name, city, network_type, geometry, capacity, pressure, age_years, status)
VALUES 
    ('Réseau eau potable Dakar Centre', 'Dakar', 'potable', 
     ST_GeomFromText('POINT(-17.4674 14.7167)', 4326), 500000, 5.2, 15, 'operational'),
    ('Réseau assainissement Plateau', 'Dakar', 'sewage',
     ST_GeomFromText('POINT(-17.4500 14.7200)', 4326), 300000, 2.8, 22, 'warning'),
    ('Système drainage Medina', 'Dakar', 'drainage',
     ST_GeomFromText('POINT(-17.4800 14.6900)', 4326), 200000, 1.5, 8, 'operational');

-- Insérer données de démonstration Abidjan

INSERT INTO spatial.water_networks (name, city, network_type, geometry, capacity, pressure, age_years, status)
VALUES 
    ('Réseau eau potable Plateau', 'Abidjan', 'potable',
     ST_GeomFromText('POINT(-4.0283 5.3364)', 4326), 800000, 5.8, 12, 'operational'),
    ('Réseau assainissement Cocody', 'Abidjan', 'sewage',
     ST_GeomFromText('POINT(-4.0100 5.3600)', 4326), 600000, 4.2, 18, 'operational');

-- Zones à risque Dakar

INSERT INTO spatial.risk_zones (name, city, risk_type, geometry, risk_level, probability, affected_population)
VALUES 
    ('Zone inondable Medina', 'Dakar', 'flood',
     ST_GeomFromText('POLYGON((-17.49 14.69, -17.48 14.69, -17.48 14.70, -17.49 14.70, -17.49 14.69))', 4326),
     'high', 35, 50000),
    ('Zone inondable Thiaroye', 'Dakar', 'flood',
     ST_GeomFromText('POLYGON((-17.43 14.75, -17.42 14.75, -17.42 14.76, -17.43 14.76, -17.43 14.75))', 4326),
     'medium', 28, 35000);

-- Zones à risque Abidjan

INSERT INTO spatial.risk_zones (name, city, risk_type, geometry, risk_level, probability, affected_population)
VALUES 
    ('Lagune Ébrié haut risque', 'Abidjan', 'flood',
     ST_GeomFromText('POLYGON((-4.02 5.33, -4.01 5.33, -4.01 5.34, -4.02 5.34, -4.02 5.33))', 4326),
     'critical', 42, 120000);

-- Chemins d'eau Dakar

INSERT INTO spatial.water_paths (name, city, path_type, geometry, width, quality, flow_rate)
VALUES 
    ('Fleuve Sénégal', 'Dakar', 'natural_river',
     ST_GeomFromText('LINESTRING(-17.5000 14.8000, -17.4000 14.7500)', 4326),
     500, 'degraded', 'seasonal'),
    ('Canal drainage Yoff', 'Dakar', 'constructed_canal',
     ST_GeomFromText('LINESTRING(-17.4800 14.6900, -17.4600 14.7000)', 4326),
     8, 'poor', 'variable');

-- Fonction pour mettre à jour updated_at
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers pour mise à jour automatique
CREATE TRIGGER trigger_water_networks_update
BEFORE UPDATE ON spatial.water_networks
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Vues pour requêtes courantes

CREATE VIEW analytics.network_summary AS
SELECT 
    city,
    network_type,
    COUNT(*) as total_networks,
    AVG(capacity) as avg_capacity,
    AVG(current_flow) as avg_flow,
    AVG(pressure) as avg_pressure,
    SUM(age_years) / COUNT(*) as avg_age
FROM spatial.water_networks
GROUP BY city, network_type;

CREATE VIEW analytics.risk_distribution AS
SELECT 
    city,
    risk_type,
    risk_level,
    COUNT(*) as zone_count,
    SUM(affected_population) as total_affected,
    AVG(probability) as avg_probability
FROM spatial.risk_zones
GROUP BY city, risk_type, risk_level;

-- Permissions (adapter selon vos besoins)
GRANT USAGE ON SCHEMA spatial TO brainblue_user;
GRANT USAGE ON SCHEMA analytics TO brainblue_user;
GRANT SELECT ON ALL TABLES IN SCHEMA spatial TO brainblue_user;
GRANT SELECT ON ALL TABLES IN SCHEMA analytics TO brainblue_user;
GRANT INSERT, UPDATE ON spatial.water_networks TO brainblue_user;
GRANT INSERT, UPDATE ON spatial.risk_zones TO brainblue_user;

-- Logs
CREATE TABLE logging.audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    table_name VARCHAR(255),
    operation VARCHAR(10),
    user_id UUID,
    old_data JSONB,
    new_data JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Statistiques et samples
ANALYZE;
