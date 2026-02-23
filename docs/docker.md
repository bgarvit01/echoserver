---
layout: page
title: Docker
nav_order: 3
permalink: /docker/
parent: Quick-Start
---

# Docker

## Basic Usage

```bash
# Run Echo Server
docker run -p 80:80 echoserver:latest

# Run in background
docker run -d -p 80:80 --name echoserver echoserver:latest

# View logs
docker logs -f echoserver
```

## Build from Source

```bash
git clone https://github.com/bgarvit01/echoserver.git
cd echoserver
docker build -t echoserver:latest .
docker run -p 80:80 echoserver:latest
```

## Environment Variables

```bash
docker run -p 80:80 \
  -e HOST=0.0.0.0 \
  -e PORT=80 \
  -e LOGS__LEVEL=info \
  -e LOGS__FORMAT=object \
  -e ENABLE_FILE=false \
  -e ENABLE_ENV=false \
  echoserver:latest
```

### Common Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `127.0.0.1` | Server bind address |
| `PORT` | `80` | Server port |
| `LOGS__LEVEL` | `debug` | Log level (debug, info, warning, error) |
| `LOGS__FORMAT` | `default` | Log format (default, line, object) |
| `ENABLE_FILE` | `true` | Enable file operations |
| `ENABLE_ENV` | `false` | Enable environment variables in response |

[See all configuration options →]({{ site.baseurl }}/configuration/)

## Volume Mounts

```bash
# Mount for file operations
docker run -p 80:80 \
  -v /tmp:/tmp:ro \
  -e ENABLE_FILE=true \
  echoserver:latest

# List directory
curl http://localhost:80/?echo_file=/tmp
```

## Security

The Docker image follows security best practices:

- ✅ Non-root user (UID 1000)
- ✅ Minimal base image (Python slim)
- ✅ Dropped capabilities
- ✅ Read-only filesystem support

### Production Security

```bash
docker run -p 80:80 \
  --memory=128m \
  --cpus="0.5" \
  --read-only \
  --tmpfs /tmp \
  --security-opt=no-new-privileges \
  echoserver:latest
```

## Health Checks

Built-in health checks are included:

```bash
# Check container health
docker ps

# Inspect health status
docker inspect echoserver | grep Health
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
# Fix volume permissions
chmod 755 /path/to/mounted/directory
```

---

**Next:** [Docker-Compose →]({{ site.baseurl }}/docker-compose/)
