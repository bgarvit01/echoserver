---
layout: page
title: Docker-Compose
nav_order: 4
permalink: /docker-compose/
parent: Quick-Start
---

# Docker-Compose

## Basic Setup

Create `docker-compose.yml`:

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
    restart: unless-stopped
```

Start the service:

```bash
# Start in foreground
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## Development Configuration

`docker-compose.dev.yml`:

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

Run:

```bash
docker-compose -f docker-compose.dev.yml up
```

## Production Configuration

`docker-compose.prod.yml`:

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

Run:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Multi-Environment Setup

Use override files for different environments:

```bash
# Base + Development
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Base + Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

## Health Checks

Add health checks to your compose file:

```yaml
services:
  echoserver:
    image: echoserver:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Rebuild and restart
docker-compose up -d --build

# Remove everything including volumes
docker-compose down -v
```

---

**Next:** [Kubernetes →]({{ site.baseurl }}/kubernetes/)
