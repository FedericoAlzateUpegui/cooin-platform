-- PostgreSQL initialization script for Cooin Backend (Production)
-- Creates necessary database extensions and configurations

-- Enable required PostgreSQL extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";
CREATE EXTENSION IF NOT EXISTS "unaccent";

-- Create indexes for better performance (will be created by Alembic migrations)
-- These are examples of what might be useful

-- Set timezone
SET timezone = 'UTC';

-- Configure database for optimal performance
-- Connection and memory settings
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET work_mem = '4MB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';

-- Checkpoint and WAL settings
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;

-- Query planner settings
ALTER SYSTEM SET random_page_cost = 1.1;
ALTER SYSTEM SET effective_io_concurrency = 200;

-- Logging configuration for production
ALTER SYSTEM SET log_min_duration_statement = 1000;  -- Log slow queries (>1s)
ALTER SYSTEM SET log_connections = on;
ALTER SYSTEM SET log_disconnections = on;
ALTER SYSTEM SET log_lock_waits = on;
ALTER SYSTEM SET log_statement = 'ddl';  -- Log DDL statements only

-- Reload configuration
SELECT pg_reload_conf();

-- Create application-specific database objects
-- (These will be created by Alembic migrations, this is just for documentation)

-- Example: Create a function for updating updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Example: Create a function for full-text search
CREATE OR REPLACE FUNCTION create_tsvector(title TEXT, content TEXT)
RETURNS TSVECTOR AS $$
BEGIN
    RETURN to_tsvector('english', COALESCE(title, '') || ' ' || COALESCE(content, ''));
END;
$$ language 'plpgsql' IMMUTABLE;

-- Grant necessary permissions to application user
GRANT USAGE, CREATE ON SCHEMA public TO cooin_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO cooin_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO cooin_user;

-- Set default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO cooin_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO cooin_user;

-- Log successful initialization
DO $$
BEGIN
    RAISE NOTICE 'Cooin database initialization completed successfully';
    RAISE NOTICE 'Extensions enabled: uuid-ossp, pg_trgm, btree_gin, unaccent';
    RAISE NOTICE 'Performance settings applied';
    RAISE NOTICE 'Database user: cooin_user configured with appropriate permissions';
END $$;