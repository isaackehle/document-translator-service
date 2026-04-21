# Local AWS Setup with LocalStack, minio, moto, and Docker/Rancher Desktop

## Overview

This document explains how to set up a local AWS development environment using LocalStack, minio, moto, and either Docker Desktop or Rancher Desktop. This setup allows you to develop and test AWS services locally without incurring costs or requiring actual AWS credentials.

## 1. Installation

### 1.1 Prerequisites
```shell
# Install Python and pip
brew install pyenv
pyenv install 3.14.4
pyenv global 3.14.4
pip install virtualenv

# brew install python
```

### 1.2 Virtual Environment Setup

#### 1.2.1 Rancher Desktop

1. Rancher Desktop Setup
```shell
# Install Rancher Desktop
brew install --cask rancher
```

2. Verify Rancher Desktop Installation
```shell
# Verify rdctl CLI is available
which rdctl

# Check rdctl version
rdctl version
```

3. Start Rancher Desktop
```shell
rdctl start --application.start-in-background

# Verify Rancher Desktop is running with rdctl
rdctl start --help
rdctl start  --containers.show-all
```
#### 1.2.2 Docker Desktop

1. Docker Desktop Setup
```shell
# Install Docker Desktop
brew install --cask docker
```

2. Verify Docker Desktop Installation

```shell
# Check if Docker Desktop is installed
which docker

# Check Docker version
docker --version

# Check if Docker daemon is running
docker info
```

3. Start Docker Desktop

```shell
# Start Docker Desktop application
open -a Docker

# Or start Docker Desktop using the CLI (if available)
# Note: Docker Desktop doesn't have a direct CLI to start the app
# but you can verify it's running with:
docker ps
```

### 1.3 LocalStack Setup
```shell
# Install LocalStack CLI (optional but recommended)
pip install localstack

# Or use Docker to run LocalStack
docker run -d \
  --name localstack \
  -p 4566:4566 \
  -p 4571:4571 \
  -e DEBUG=1 \
  localstack/localstack:latest
```

### 1.4 MinIO Setup
```shell
# Run minio
docker run -d \
  --name minio \
  -p 9000:9000 \
  -p 9001:9001 \
  -e "MINIO_ROOT_USER=minioadmin" \
  -e "MINIO_ROOT_PASSWORD=minioadmin" \
  minio/minio server /data --console-address ":9001"
```

### 1.5 Moto Setup
```shell
# Install moto in your Python environment
pip install moto
```

### 1.9 Account Setup

#### LocalStack's authentication model

The localstack/localstack:latest Docker image now requires a `LOCALSTACK_AUTH_TOKEN` for startup, even for community (free) usage.

Use a Free Auth Token (Recommended):

1. Create a free account at https://app.localstack.cloud
2. Generate an Auth Token:
  a. Go to Settings → Auth Tokens
  b. Create and copy your token
  c. Set the token in your environment:

in `~/.env.local`

```shell
export LOCALSTACK_AUTH_TOKEN=`LOCALSTACK_AUTH_TOKEN`
```


## 2. Configuration

### 2.1 Docker Compose Setup
Create `docker-compose.yml`:

```yaml
services:
  localstack:
    image: localstack/localstack:latest
    ports:
      - "4566:4566"
      - "4571:4571"
    environment:
      - DEBUG=1
      - DOCKER_HOST=unix:///var/run/docker.sock
      - LOCALSTACK_AUTH_TOKEN=${LOCALSTACK_AUTH_TOKEN}
    volumes:
      - "${LOCALSTACK_VOLUME_DIR:-./volume}:/var/lib/localstack"
      - "/var/run/docker.sock:/var/run/docker.sock"

  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      - "MINIO_ROOT_USER=minioadmin"
      - "MINIO_ROOT_PASSWORD=minioadmin"
    command: server /data --console-address ":9001"
    volumes:
      - "minio_data:/data"

volumes:
  minio_data:
```

### 2.2 AWS Configuration
Create `~/.aws/credentials`:

```ini
[local]
aws_access_key_id = test
aws_secret_access_key = test
region = us-east-1
```

Create `~/.aws/config`:

```ini
[profile local]
region = us-east-1
output = json
```

## 3. Start / Usage

### 3.1 Starting the Services
```shell
# Start all services with Docker Compose
docker-compose up -d

# Verify services are running
docker-compose ps
```

### 3.2 Testing the Setup
```shell
# Test LocalStack health
curl http://localhost:4566/health

# Test minio
curl http://localhost:9000/minio/health/live

# Test boto3 connection
python3 -c "
import boto3
from moto import mock_s3

# Test with moto
with mock_s3():
    s3 = boto3.client('s3', region_name='us-east-1')
    s3.create_bucket(Bucket='test-bucket')
    print('S3 mock test passed')
"
```

## 4. Container Grouping and Image Management

To organize and manage containers for this project effectively, we recommend using Docker Compose with a project name. This groups all containers related to this project under a single namespace.

### 4.1 Using Docker Compose Project Names

When starting the containers, use a project name to group them:

```shell
# Start all services with a specific project name
docker-compose -p local-aws-project up -d

# Stop all services in the project
docker-compose -p local-aws-project down

# View containers in the project
docker-compose -p local-aws-project ps
```

### 4.2 Creating a Custom Docker Compose File with Labels

You can also add labels to your services to help identify them:

```yaml
version: '3.8'
services:
  localstack:
    image: localstack/localstack:latest
    ports:
      - "4566:4566"
      - "4571:4571"
    environment:
      - DEBUG=1
      - DOCKER_HOST=unix:///var/run/docker.sock
    volumes:
      - "${LOCALSTACK_VOLUME_DIR:-./volume}:/var/lib/localstack"
      - "/var/run/docker.sock:/var/run/docker.sock"
    labels:
      - "project=local-aws-setup"
      - "service=localstack"

  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      - "MINIO_ROOT_USER=minioadmin"
      - "MINIO_ROOT_PASSWORD=minioadmin"
    command: server /data --console-address ":9001"
    volumes:
      - "minio_data:/data"
    labels:
      - "project=local-aws-setup"
      - "service=minio"

volumes:
  minio_data:
```

### 4.3 Managing Containers by Group

Once your containers are grouped, you can manage them by project:

```shell
# List all containers for this project
docker ps --filter "label=project=local-aws-setup"

# Stop all containers in the project
docker stop $(docker ps -q --filter "label=project=local-aws-setup")

# Remove all containers in the project
docker rm $(docker ps -aq --filter "label=project=local-aws-setup")
```

## 5. Working with Rancher Desktop Image Groups

When using Rancher Desktop, you can create and manage images within the same group for better organization and management.

### 5.1 Creating Images in the Same Group

To create new images that belong to the same group as your existing containers:

1. Build a new image using the same project context:

```shell
# Build a new image with a specific tag
docker build -t local-aws-project/my-service:latest .

# Or build with a specific project name
docker build -t local-aws-project/my-service:v1.0 .
```

2. Run the new image within the same project:

```shell
# Run the new container with the project name
docker run -d --name my-service \
  --network local-aws-project_default \
  local-aws-project/my-service:latest
```

### 5.2 Managing Images in Rancher Desktop

In Rancher Desktop, you can manage images through:

1. **Using the Rancher Desktop UI:**
   - Open Rancher Desktop
   - Navigate to the "Images" tab
   - View all images grouped under your project
   - Delete or manage images as needed

2. **Using CLI commands:**
   ```shell
   # List all images
   docker images

   # Filter images by project
   docker images --filter "reference=local-aws-project/*"

   # Remove specific images
   docker rmi local-aws-project/my-service:latest
   ```

### 5.3 Best Practices for Image Grouping

1. **Use consistent naming conventions:**
   ```shell
   # Use project prefix for all images
   local-aws-project/service-name:tag
   ```

2. **Tag images appropriately:**
   ```shell
   # Use semantic versioning or timestamps
   local-aws-project/api-service:v1.2.0
   local-aws-project/api-service:2023-10-15
   ```

3. **Clean up unused images:**
   ```shell
   # Remove dangling images
   docker image prune

   # Remove images not used by any container
   docker image prune -a
   ```

## 6. Verification

### 6.1 Verify Docker Installation
```shell
# Check Docker version
docker --version

# Check if Docker daemon is running
docker info
```


### 6.2 Verify LocalStack Installation
```shell
# Check LocalStack version
localstack --version

# Test LocalStack health
curl http://localhost:4566/health
```

### 6.3 Verify MinIO Installation
```shell
# Test MinIO health
curl http://localhost:9000/minio/health/live
```

### 6.4 Verify Moto Installation
```shell
# Check if moto is installed
pip show moto

# Test moto in Python
python3 -c "import moto; print('Moto installed successfully')"
```

## References

- [Docker Documentation](https://docs.docker.com/)
- [Rancher Desktop Documentation](https://rancherdesktop.io/)
- [LocalStack Documentation](https://docs.localstack.cloud/)
- [MinIO Documentation](https://min.io/docs/)
- [Moto Documentation](https://docs.getmoto.org/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)