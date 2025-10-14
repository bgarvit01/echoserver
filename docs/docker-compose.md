---
layout: page
title: Docker Compose
permalink: /docker-compose/
---

# Docker Compose Deployment

Deploy Echo Server using Docker Compose for easy multi-environment setups.

## Basic Setup

### docker-compose.yml
```yaml
version: "3.8"

services:
  echoserver:
    build: .
    ports:
      - "80:80"
    environment:
      - LOGS__LEVEL=info
      - LOGS__FORMAT=object
    restart: unless-stopped
```

### Start the Service
```bash
# Start in foreground
docker-compose up

# Start in background
docker-compose up -d

# Stop the service
docker-compose down
```

## Development Configuration

Create a `docker-compose.dev.yml`:

```yaml
version: "3.8"

services:
  echoserver:
    build: .
    ports:
      - "80:80"
    environment:
      - LOGS__LEVEL=debug
      - LOGS__FORMAT=default
      - ENABLE_FILE=true
      - ENABLE_ENV=true
    volumes:
      - ./:/app
    restart: unless-stopped
```

### Run Development Setup
```bash
docker-compose -f docker-compose.dev.yml up
```

## Production Configuration

Create a `docker-compose.prod.yml`:

```yaml
version: "3.8"

services:
  echoserver:
    image: echoserver:latest
    ports:
      - "80:80"
    environment:
      - LOGS__LEVEL=info
      - LOGS__FORMAT=object
      - ENABLE_FILE=false
      - ENABLE_ENV=false
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 128M
    restart: always
    read_only: true
    tmpfs:
      - /tmp
    security_opt:
      - no-new-privileges:true
```

### Run Production Setup
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Testing

```bash
# Test the service
curl http://localhost:80

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

## Cleanup

```bash
# Stop and remove containers
docker-compose down

# Stop, remove containers, and volumes
docker-compose down -v
```

