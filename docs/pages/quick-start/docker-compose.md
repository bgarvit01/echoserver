---
layout: default
title: Docker Compose
parent: Quick Start
nav_order: 2
---

# Docker Compose

Deploy Echo Server using Docker Compose for multi-environment setups.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Available Configurations

Echo Server includes three Docker Compose configurations:

- **Basic** (`docker-compose.yml`) - Simple setup
- **Development** (`docker-compose.dev.yml`) - Development environment
- **Production** (`docker-compose.prod.yml`) - Production ready

## Development Environment

Perfect for development and testing with debugging features enabled.

### Start Development Environment
```bash
cd docker-compose
docker-compose -f docker-compose.dev.yml up

# Run in background
docker-compose -f docker-compose.dev.yml up -d

# With rebuild
docker-compose -f docker-compose.dev.yml up --build
```

### Development Features
- **Debug logging** enabled
- **File operations** enabled for testing
- **Environment variables** exposed
- **Volume mounting** for live code changes
- **Human-readable** log format

## Production Environment

Optimized for production deployment with security and performance focus.

### Start Production Environment
```bash
cd docker-compose
docker-compose -f docker-compose.prod.yml up -d

# Scale to multiple replicas
docker-compose -f docker-compose.prod.yml up -d --scale echo-server=5
```

### Production Features
- **Security-focused** configuration
- **File operations** disabled
- **Environment variables** hidden
- **Structured logging** for log aggregation
- **Health checks** and restart policies
- **Resource limits** applied

## Basic Configuration

Simple single-container setup for quick testing.

```bash
cd docker-compose
docker-compose up -d
```

## Configuration Override

Create a `docker-compose.override.yml` file for local customizations:

```yaml
version: "3.8"

services:
  echo-server:
    ports:
      - "8080:80"  # Use different port
    environment:
      - LOGS__LEVEL=debug
      - ENABLE_FILE=true
    volumes:
      - ./custom-data:/data
```

## Environment Variables

### Development Settings
```yaml
environment:
  - LOGS__LEVEL=debug
  - LOGS__FORMAT=default
  - ENABLE_LOGS=true
  - ENABLE_FILE=true
  - ENABLE_ENV=true
```

### Production Settings
```yaml
environment:
  - LOGS__LEVEL=info
  - LOGS__FORMAT=object
  - ENABLE_LOGS=true
  - ENABLE_FILE=false
  - ENABLE_ENV=false
  - CONTROLS__TIMES__MAX=10000
```

## Examples

### Basic Usage
```bash
# Start the service
docker-compose up -d

# Test the service
curl http://localhost:80

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

### Development Workflow
```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# Test with file operations
curl http://localhost:80/?echo_file=/tmp

# Test environment variables
curl http://localhost:80/?echo_env_body=HOSTNAME

# View detailed logs
docker-compose -f docker-compose.dev.yml logs -f echo-server
```

### Production Deployment
```bash
# Deploy production stack
docker-compose -f docker-compose.prod.yml up -d

# Scale to 5 replicas
docker-compose -f docker-compose.prod.yml up -d --scale echo-server=5

# Check service health
docker-compose -f docker-compose.prod.yml ps

# Update configuration
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
```

## Health Checks

All configurations include health checks:

```bash
# Check container health
docker-compose ps

# View health check logs
docker-compose logs echo-server | grep health
```

## Scaling

### Manual Scaling
```bash
# Scale up
docker-compose up -d --scale echo-server=3

# Scale down
docker-compose up -d --scale echo-server=1
```

### Load Balancing
When scaling, Docker Compose automatically load balances between replicas:

```bash
# Start multiple replicas
docker-compose -f docker-compose.prod.yml up -d --scale echo-server=3

# Test load balancing
for i in {1..10}; do
  curl -s http://localhost:80 | jq -r '.host.hostname'
done
```

## Troubleshooting

### Service Won't Start
```bash
# Check logs
docker-compose logs echo-server

# Check configuration
docker-compose config

# Validate compose file
docker-compose -f docker-compose.dev.yml config
```

### Port Conflicts
```bash
# Check what's using the port
lsof -i :80

# Use different port in override file
echo "
version: '3.8'
services:
  echo-server:
    ports:
      - '8080:80'
" > docker-compose.override.yml
```

### Resource Issues
```bash
# Check resource usage
docker stats

# Add resource limits to compose file
echo "
    deploy:
      resources:
        limits:
          memory: 128M
          cpus: '0.5'
" >> docker-compose.yml
```
