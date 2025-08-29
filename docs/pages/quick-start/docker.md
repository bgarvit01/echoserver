---
layout: default
title: Docker
parent: Quick Start
nav_order: 1
---

# Docker

Deploy Echo Server using Docker containers.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Build from Source

### Clone and Build
```bash
# Clone the repository
git clone https://github.com/bgarvit01/echoserver.git
cd echoserver

# Build the image
docker build -t echoserver:latest .
```

### Run Container
```bash
# Run with default settings (port 80)
docker run -p 80:80 echoserver:latest

# Run in background
docker run -d -p 80:80 --name echoserver echoserver:latest
```

## Pre-built Images

```bash
# Pull and run (replace with your registry)
docker pull your-registry/echoserver:latest
docker run -p 80:80 your-registry/echoserver:latest
```

## Configuration

### Environment Variables
```bash
# Run with custom configuration
docker run -p 80:80 \
  -e LOGS__LEVEL=info \
  -e LOGS__FORMAT=object \
  -e ENABLE_FILE=false \
  -e ENABLE_ENV=false \
  echoserver:latest
```

### Volume Mounts
```bash
# Mount directories for file operations
docker run -p 80:80 \
  -v /tmp:/tmp:ro \
  -e ENABLE_FILE=true \
  echoserver:latest
```

## Health Checks

The Docker image includes built-in health checks:

```bash
# Check container health
docker ps
docker inspect echoserver | grep Health

# View health check logs
docker logs echoserver
```

## Examples

### Basic Echo
```bash
# Start the server
docker run -d -p 80:80 --name echoserver echoserver:latest

# Test basic functionality
curl http://localhost:80
```

### Custom Response
```bash
# Custom status code
curl -I http://localhost:80/?echo_code=404

# Custom body
curl http://localhost:80/?echo_body=hello

# Custom headers
curl -I http://localhost:80/?echo_header=Custom:Value
```

### File Operations
```bash
# Enable file operations
docker run -d -p 80:80 \
  -v /tmp:/tmp:ro \
  -e ENABLE_FILE=true \
  --name echoserver \
  echoserver:latest

# List directory
curl http://localhost:80/?echo_file=/tmp
```

## Security Considerations

The Docker image follows security best practices:

- **Non-root user**: Runs as user ID 1000
- **Minimal base image**: Based on Python slim image
- **Read-only filesystem**: Where possible
- **Dropped capabilities**: All unnecessary capabilities removed
- **Resource limits**: Memory and CPU limits recommended

### Production Security
```bash
# Run with security constraints
docker run -p 80:80 \
  --memory=128m \
  --cpus="0.5" \
  --read-only \
  --tmpfs /tmp \
  --security-opt=no-new-privileges \
  echoserver:latest
```

## Troubleshooting

### Container Won't Start
```bash
# Check logs
docker logs echoserver

# Check if port is available
lsof -i :80
```

### Permission Issues
```bash
# Check if volume mounts have correct permissions
ls -la /path/to/mounted/directory

# Fix permissions if needed
sudo chmod 755 /path/to/mounted/directory
```

### Network Issues
```bash
# Check container networking
docker inspect echoserver | grep IPAddress

# Test from inside container
docker exec -it echoserver curl http://localhost:80
```
