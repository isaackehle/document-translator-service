#!/bin/bash
# start-localstack.sh
# Start LocalStack with safe defaults and environment variable handling
# Usage: ./start-localstack.sh [start|stop|status]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
ENV_FILE="${PROJECT_DIR}/.env"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Load environment variables if .env exists
load_env() {
    if [[ -f "$ENV_FILE" ]]; then
        log_info "Loading environment from $ENV_FILE"
        set -a
        source "$ENV_FILE"
        set +a
    else
        log_warn "No .env file found. Using defaults."
    fi
}

# Validate required environment variables
validate_env() {
    if [[ -z "${LOCALSTACK_AUTH_TOKEN:-}" ]]; then
        log_error "LOCALSTACK_AUTH_TOKEN is not set"
        log_info "Please set it in your .env file or export it before running"
        exit 1
    fi
}

# Start LocalStack
start_localstack() {
    log_info "Starting LocalStack..."
    
    docker-compose up -d localstack
    
    log_info "Waiting for LocalStack to be ready..."
    sleep 5
    
    if check_localstack_health; then
        log_info "LocalStack is ready!"
        log_info "API: http://localhost:4567"
        log_info "Health: http://localhost:4567/_localstack/health"
        log_info "LocalStack CLI: awslocal --endpoint-url=http://localhost:4567"
    else
        log_error "LocalStack failed to start"
        exit 1
    fi
}

# Stop LocalStack
stop_localstack() {
    log_info "Stopping LocalStack..."
    docker-compose down localstack
    log_info "LocalStack stopped"
}

# Check LocalStack health
check_localstack_health() {
    local max_attempts=30
    local attempt=1
    
    while [[ $attempt -le $max_attempts ]]; do
        if curl -s -f "http://localhost:4567/_localstack/health" > /dev/null 2>&1; then
            return 0
        fi
        log_info "Waiting for LocalStack... (attempt $attempt/$max_attempts)"
        sleep 2
        ((attempt++))
    done
    
    return 1
}

# Show LocalStack status
show_status() {
    if check_localstack_health; then
        log_info "LocalStack is running"
        log_info "Endpoints:"
        log_info "  - API: http://localhost:4567"
        log_info "  - Health: http://localhost:4567/_localstack/health"
    else
        log_warn "LocalStack is not running"
    fi
}

# Main command handler
main() {
    load_env
    validate_env
    
    case "${1:-start}" in
        start)
            start_localstack
            ;;
        stop)
            stop_localstack
            ;;
        status)
            show_status
            ;;
        restart)
            stop_localstack
            start_localstack
            ;;
        *)
            log_error "Unknown command: $1"
            log_info "Usage: $0 [start|stop|status|restart]"
            exit 1
            ;;
    esac
}

main "$@"
