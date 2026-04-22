#!/bin/bash
# start-localstack.sh
# Safe LocalStack startup with sensible defaults for development

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting LocalStack...${NC}"

# Use docker-compose if available, otherwise use localstack CLI
if command -v docker-compose &> /dev/null; then
    echo "Using docker-compose to start LocalStack"
    docker-compose up -d localstack
elif docker compose ls &> /dev/null; then
    echo "Using docker compose (v2) to start LocalStack"
    docker compose up -d localstack
else
    echo -e "${RED}Error: Neither docker-compose nor docker compose v2 found${NC}"
    exit 1
fi

# Wait for LocalStack to be ready
echo -e "${YELLOW}Waiting for LocalStack to be ready...${NC}"
MAX_RETRIES=30
RETRY_INTERVAL=2
RETRIES=0

while ! curl -s http://localhost:4566/health &> /dev/null; do
    RETRIES=$((RETRIES + 1))
    if [ $RETRIES -ge $MAX_RETRIES ]; then
        echo -e "${RED}LocalStack did not start within $((MAX_RETRIES * RETRY_INTERVAL)) seconds${NC}"
        exit 1
    fi
    sleep $RETRY_INTERVAL
done

echo -e "${GREEN}LocalStack is ready!${NC}"

# Optional: Initialize AWS resources
if [ -f "aws-resources.sh" ]; then
    echo -e "${YELLOW}Running AWS resource initialization...${NC}"
    chmod +x aws-resources.sh
    ./aws-resources.sh
fi

echo -e "${GREEN}LocalStack started successfully${NC}"
