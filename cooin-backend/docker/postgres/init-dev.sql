-- PostgreSQL initialization script for Cooin Backend (Development)
-- Creates necessary database extensions and development-friendly configurations

-- Enable required PostgreSQL extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";
CREATE EXTENSION IF NOT EXISTS "unaccent";

-- Set timezone
SET timezone = 'UTC';

-- Development-friendly database configuration
-- Less restrictive settings for development
ALTER SYSTEM SET max_connections = 100;
ALTER SYSTEM SET shared_buffers = '128MB';
ALTER SYSTEM SET work_mem = '2MB';

-- Development logging - more verbose for debugging
ALTER SYSTEM SET log_statement = 'all';  -- Log all statements
ALTER SYSTEM SET log_min_duration_statement = 0;  -- Log all queries
ALTER SYSTEM SET log_connections = on;
ALTER SYSTEM SET log_disconnections = on;
ALTER SYSTEM SET log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h ';

-- Reload configuration
SELECT pg_reload_conf();

-- Create development helper functions
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create function for full-text search
CREATE OR REPLACE FUNCTION create_tsvector(title TEXT, content TEXT)
RETURNS TSVECTOR AS $$
BEGIN
    RETURN to_tsvector('english', COALESCE(title, '') || ' ' || COALESCE(content, ''));
END;
$$ language 'plpgsql' IMMUTABLE;

-- Grant permissions to development user
GRANT USAGE, CREATE ON SCHEMA public TO cooin_dev;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO cooin_dev;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO cooin_dev;

-- Set default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO cooin_dev;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO cooin_dev;

-- Create some sample data for development (optional)
-- This will be populated by Alembic migrations and test data

-- Log successful initialization
DO $$
BEGIN
    RAISE NOTICE '=== Cooin Development Database Initialization ===';
    RAISE NOTICE 'Extensions enabled: uuid-ossp, pg_trgm, btree_gin, unaccent';
    RAISE NOTICE 'Development logging enabled (all statements)';
    RAISE NOTICE 'Database user: cooin_dev configured with full permissions';
    RAISE NOTICE 'Ready for development!';
END $$;