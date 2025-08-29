---
layout: default
title: Loggers
parent: Configuration
nav_order: 2
---

# Loggers

Echo Server provides flexible logging configuration with multiple formats and levels for different environments.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Log Levels

### Available Levels
- **`debug`** - Detailed information for debugging (default)
- **`info`** - General information about server operation
- **`warning`** - Warning messages for potential issues
- **`error`** - Error messages for failures

### Setting Log Level

#### Environment Variable
```bash
export LOGS__LEVEL=info
```

#### Command Line
```bash
python run_server.py --log-level info
```

#### Docker
```bash
docker run -e LOGS__LEVEL=info echoserver:latest
```

## Log Formats

Echo Server supports three log formats optimized for different use cases.

### Default Format
**Environment Variable:** `LOGS__FORMAT=default`  
**Use Case:** Development and human-readable logs

```
2024-01-15 10:30:45 - echoserver - INFO - Server starting on 127.0.0.1:80
2024-01-15 10:30:45 - echoserver - INFO - All features enabled
2024-01-15 10:30:46 - echoserver - INFO - GET / - 200 - 1.23ms
```

### Line Format
**Environment Variable:** `LOGS__FORMAT=line`  
**Use Case:** Single-line logs for log aggregation systems

```
2024-01-15T10:30:45.123Z INFO echoserver Server starting on 127.0.0.1:80
2024-01-15T10:30:45.124Z INFO echoserver All features enabled
2024-01-15T10:30:46.456Z INFO echoserver GET / 200 1.23ms
```

### Object Format (JSON)
**Environment Variable:** `LOGS__FORMAT=object`  
**Use Case:** Structured logging for log analysis and monitoring systems

```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "INFO",
  "app": "echoserver",
  "message": "Server starting on 127.0.0.1:80",
  "host": "echoserver-pod-123",
  "pid": 1234
}
{
  "timestamp": "2024-01-15T10:30:46.456Z",
  "level": "INFO",
  "app": "echoserver",
  "message": "Request processed",
  "method": "GET",
  "path": "/",
  "status": 200,
  "duration": 1.23,
  "client_ip": "192.168.1.100"
}
```

## Application Name

Customize the application name in logs:

```bash
export LOGS__APP=my-echoserver
```

## Configuration Examples

### Development Environment
```bash
export LOGS__LEVEL=debug
export LOGS__FORMAT=default
export LOGS__APP=echo-dev
```

Output:
```
2024-01-15 10:30:45 - echo-dev - DEBUG - Configuration loaded: ServerConfig(host='127.0.0.1', port=80)
2024-01-15 10:30:45 - echo-dev - DEBUG - Feature flags: {'enable_logs': True, 'enable_file': True}
2024-01-15 10:30:45 - echo-dev - INFO - Server starting on 127.0.0.1:80
```

### Production Environment
```bash
export LOGS__LEVEL=info
export LOGS__FORMAT=object
export LOGS__APP=echo-prod
```

Output:
```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "INFO",
  "app": "echo-prod",
  "message": "Server starting on 127.0.0.1:80",
  "environment": "production"
}
```

### Log Aggregation (ELK Stack)
```bash
export LOGS__LEVEL=info
export LOGS__FORMAT=object
export LOGS__APP=echoserver
```

Perfect for Elasticsearch, Logstash, and Kibana integration.

## Docker Configuration

### Basic Docker Logging
```bash
docker run -p 80:80 \
  -e LOGS__LEVEL=info \
  -e LOGS__FORMAT=line \
  echoserver:latest
```

### Docker Compose
```yaml
version: "3.8"
services:
  echoserver:
    image: echoserver:latest
    environment:
      - LOGS__LEVEL=info
      - LOGS__FORMAT=object
      - LOGS__APP=echo-docker
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Docker with Log Driver
```bash
docker run -p 80:80 \
  -e LOGS__FORMAT=object \
  --log-driver=fluentd \
  --log-opt fluentd-address=localhost:24224 \
  --log-opt tag="echoserver" \
  echoserver:latest
```

## Kubernetes Configuration

### ConfigMap for Logging
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: echoserver-logging-config
data:
  LOGS__LEVEL: "info"
  LOGS__FORMAT: "object"
  LOGS__APP: "echo-k8s"
```

### Deployment with Logging
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: echoserver
spec:
  template:
    spec:
      containers:
      - name: echoserver
        image: echoserver:latest
        envFrom:
        - configMapRef:
            name: echoserver-logging-config
```

### Viewing Logs
```bash
# View logs from all pods
kubectl logs -l app=echoserver

# Follow logs
kubectl logs -l app=echoserver -f

# View logs with timestamps
kubectl logs -l app=echoserver --timestamps=true

# View recent logs
kubectl logs -l app=echoserver --since=1h
```

## Advanced Configuration

### Values File
```yaml
# values.yaml
echoServer:
  logs:
    level: "info"
    format: "object"
    app: "echo-helm"
```

