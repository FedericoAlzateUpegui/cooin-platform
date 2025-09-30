#!/bin/bash

# Cooin Backend Deployment Script
# Automates the deployment process for production

set -e  # Exit on any error

# Configuration
APP_NAME="cooin-backend"
BACKUP_DIR="/opt/cooin/backups"
LOG_FILE="/opt/cooin/logs/deploy.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}" | tee -a "$LOG_FILE"
    exit 1
}

warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}" | tee -a "$LOG_FILE"
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}" | tee -a "$LOG_FILE"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        error "This script should not be run as root. Please run as a regular user with sudo privileges."
    fi
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."

    # Check Docker
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Please install Docker first."
    fi

    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        error "Docker Compose is not installed. Please install Docker Compose first."
    fi

    # Check if .env file exists
    if [[ ! -f .env ]]; then
        error ".env file not found. Please create it from .env.example"
    fi

    log "Prerequisites check passed"
}

# Create necessary directories
create_directories() {
    log "Creating necessary directories..."

    sudo mkdir -p "$BACKUP_DIR"
    sudo mkdir -p "/opt/cooin/logs"
    sudo mkdir -p "/opt/cooin/ssl"
    sudo mkdir -p "/opt/cooin/uploads"

    # Set permissions
    sudo chown -R $USER:$USER /opt/cooin/

    log "Directories created successfully"
}

# Backup database
backup_database() {
    log "Creating database backup..."

    # Get database credentials from .env
    source .env

    # Create backup filename with timestamp
    BACKUP_FILE="$BACKUP_DIR/cooin_backup_$(date +%Y%m%d_%H%M%S).sql"

    # Create database backup
    if docker-compose exec -T postgres pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" > "$BACKUP_FILE"; then
        log "Database backup created: $BACKUP_FILE"
    else
        warning "Database backup failed, but continuing with deployment"
    fi
}

# Pull latest images
pull_images() {
    log "Pulling latest Docker images..."

    docker-compose pull

    log "Docker images updated successfully"
}

# Run database migrations
run_migrations() {
    log "Running database migrations..."

    # Stop existing migrations container if running
    docker-compose stop migrations 2>/dev/null || true
    docker-compose rm -f migrations 2>/dev/null || true

    # Run migrations
    docker-compose run --rm migrations

    log "Database migrations completed"
}

# Deploy application
deploy_app() {
    log "Deploying application..."

    # Build and start services
    docker-compose up -d --build

    log "Application deployed successfully"
}

# Health check
health_check() {
    log "Performing health check..."

    local max_attempts=30
    local attempt=1

    while [[ $attempt -le $max_attempts ]]; do
        if curl -f http://localhost:8000/api/v1/health &> /dev/null; then
            log "Health check passed"
            return 0
        fi

        info "Health check attempt $attempt/$max_attempts failed, retrying in 10 seconds..."
        sleep 10
        ((attempt++))
    done

    error "Health check failed after $max_attempts attempts"
}

# Clean up old images and containers
cleanup() {
    log "Cleaning up old images and containers..."

    # Remove stopped containers
    docker container prune -f

    # Remove unused images
    docker image prune -f

    # Remove old backups (keep last 7 days)
    find "$BACKUP_DIR" -name "cooin_backup_*.sql" -mtime +7 -delete 2>/dev/null || true

    log "Cleanup completed"
}

# Main deployment function
main() {
    log "Starting Cooin Backend deployment..."

    check_root
    check_prerequisites
    create_directories

    # Ask for confirmation
    echo -e "${YELLOW}This will deploy the Cooin Backend to production. Continue? (y/N)${NC}"
    read -r confirmation
    if [[ ! "$confirmation" =~ ^[Yy]$ ]]; then
        log "Deployment cancelled by user"
        exit 0
    fi

    # Perform backup if database is running
    if docker-compose ps postgres | grep -q "Up"; then
        backup_database
    fi

    pull_images
    run_migrations
    deploy_app

    # Wait a moment for services to start
    sleep 10

    health_check
    cleanup

    log "Cooin Backend deployment completed successfully!"

    # Show running services
    echo -e "${GREEN}Running services:${NC}"
    docker-compose ps

    echo -e "${GREEN}Deployment Summary:${NC}"
    echo "- API: http://localhost:8000"
    echo "- Health Check: http://localhost:8000/api/v1/health"
    echo "- Logs: docker-compose logs -f"
    echo "- Stop: docker-compose down"
}

# Handle script arguments
case "${1:-}" in
    "backup")
        backup_database
        ;;
    "health")
        health_check
        ;;
    "cleanup")
        cleanup
        ;;
    "")
        main
        ;;
    *)
        echo "Usage: $0 [backup|health|cleanup]"
        echo "  backup  - Create database backup only"
        echo "  health  - Run health check only"
        echo "  cleanup - Clean up old images and containers"
        echo "  (no args) - Full deployment"
        exit 1
        ;;
esac