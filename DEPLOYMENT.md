# Echo Server Deployment Guide

This guide provides comprehensive instructions for deploying the Echo Server using Docker, Docker Compose, Kubernetes, and Helm.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Docker](#docker)
- [Docker Compose](#docker-compose)
- [Kubernetes](#kubernetes)
- [Helm](#helm)
- [Configuration](#configuration)
- [Monitoring and Health Checks](#monitoring-and-health-checks)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- Docker Engine 20.10+ (for Docker deployments)
- Docker Compose 2.0+ (for Compose deployments)
- Kubernetes 1.19+ (for K8s deployments)
- Helm 3.0+ (for Helm deployments)
- kubectl configured for your cluster

## Docker

### Building the Image

```bash
# Build from source
docker build -t echo-server:latest .

# Build with specific tag
docker build -t echo-server:v2.0.0 .
```

### Running Containers

#### Basic Usage
```bash
# Run with default configuration
docker run -p 80:80 echo-server:latest

# Run in background
docker run -d -p 80:80 --name echo-server echo-server:latest
```

#### Advanced Configuration
```bash
# Run with custom environment variables
docker run -p 80:80 \
  -e LOGS__LEVEL=info \
  -e LOGS__FORMAT=object \
  -e ENABLE_FILE=false \
  -e ENABLE_ENV=false \
  -e CONTROLS__TIMES__MAX=10000 \
  echo-server:latest

# Run with volume mounts (for file operations)
docker run -p 80:80 \
  -v /tmp:/tmp:ro \
  -e ENABLE_FILE=true \
  echo-server:latest
```

#### Health Checks
```bash
# Check container health
docker ps
docker inspect echo-server | grep Health

# View logs
docker logs echo-server
```

## Docker Compose

### Development Environment

```bash
# Start development environment
cd docker-compose
docker-compose -f docker-compose.dev.yml up

# Run in background
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f
```

### Production Environment

```bash
# Start production environment
cd docker-compose
docker-compose -f docker-compose.prod.yml up -d

# Scale to multiple replicas
docker-compose -f docker-compose.prod.yml up -d --scale echo-server=3

# Update configuration
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
```

### Compose Commands

```bash
# Stop services
docker-compose down

# Rebuild and restart
docker-compose up --build

# View service status
docker-compose ps

# Execute commands in container
docker-compose exec echo-server python --version
```

## Kubernetes

### Quick Deployment

Deploy everything with a single command:

```bash
# From URL (replace with your repository)
kubectl apply -f https://raw.githubusercontent.com/yourrepo/echoserver/main/k8s/echo-server-all.yaml

# From local file
kubectl apply -f k8s/echo-server-all.yaml
```

### Step-by-Step Deployment

```bash
# 1. Create namespace
kubectl apply -f k8s/namespace.yaml

# 2. Create configuration
kubectl apply -f k8s/configmap.yaml

# 3. Deploy application
kubectl apply -f k8s/deployment.yaml

# 4. Create service
kubectl apply -f k8s/service.yaml

# 5. Create ingress (optional)
kubectl apply -f k8s/ingress.yaml
```

### Verification

```bash
# Check deployment status
kubectl get pods -n echo-server
kubectl get svc -n echo-server
kubectl get ingress -n echo-server

# View logs
kubectl logs -n echo-server deployment/echo-server

# Port forward for testing
kubectl port-forward -n echo-server service/echo-server-service 80:80
```

### Scaling

```bash
# Scale deployment
kubectl scale deployment echo-server -n echo-server --replicas=5

# Check scaling status
kubectl get deployment echo-server -n echo-server
```

### Configuration Updates

```bash
# Update ConfigMap
kubectl apply -f k8s/configmap.yaml

# Restart deployment to pick up changes
kubectl rollout restart deployment/echo-server -n echo-server

# Check rollout status
kubectl rollout status deployment/echo-server -n echo-server
```

## Helm

### Installation

#### From Local Chart

```bash
# Install with default values
helm install my-echo-server ./helm/echo-server

# Install in specific namespace
helm install my-echo-server ./helm/echo-server --namespace echo-server --create-namespace

# Install with custom values
helm install my-echo-server ./helm/echo-server \
  --set replicaCount=3 \
  --set echoServer.logs.level=info \
  --set ingress.enabled=true
```

#### From Helm Repository

```bash
# Add repository (replace with actual repo)
helm repo add echo-server https://your-helm-repo/charts
helm repo update

# Install from repo
helm install my-echo-server echo-server/echo-server
```

### Custom Values

Create a `values.yaml` file:

```yaml
# values-production.yaml
replicaCount: 3

image:
  repository: your-registry/echo-server
  tag: "v2.0.0"

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: echo.yourdomain.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: echo-server-tls
      hosts:
        - echo.yourdomain.com

echoServer:
  logs:
    level: "info"
    format: "object"
  features:
    enableFile: false
    enableEnv: false
  controls:
    timesMax: 10000

resources:
  limits:
    cpu: 500m
    memory: 256Mi
  requests:
    cpu: 200m
    memory: 128Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

Install with custom values:

```bash
helm install my-echo-server ./helm/echo-server -f values-production.yaml
```

### Helm Management

```bash
# List installations
helm list

# Get installation status
helm status my-echo-server

# Upgrade installation
helm upgrade my-echo-server ./helm/echo-server -f values-production.yaml

# Rollback to previous version
helm rollback my-echo-server 1

# Uninstall
helm uninstall my-echo-server
```

## Configuration

### Environment Variables

| Variable | Description | Default | Examples |
|----------|-------------|---------|----------|
| `HOST` | Bind host | `0.0.0.0` | `127.0.0.1` |
| `PORT` | Bind port | `80` | `8080` |
| `LOGS__LEVEL` | Log level | `debug` | `info`, `warning`, `error` |
| `LOGS__FORMAT` | Log format | `default` | `line`, `object` |
| `ENABLE_LOGS` | Enable logging | `true` | `false` |
| `ENABLE_FILE` | Enable file operations | `true` | `false` |
| `ENABLE_ENV` | Show environment variables | `false` | `true` |
| `CONTROLS__TIMES__MAX` | Max delay (ms) | `60000` | `30000` |

### Security Considerations

#### Production Settings
```bash
# Recommended production environment variables
LOGS__LEVEL=info
LOGS__FORMAT=object
ENABLE_FILE=false
ENABLE_ENV=false
CONTROLS__TIMES__MAX=10000
```

#### Container Security
- Runs as non-root user (UID 1000)
- Drops all capabilities
- Read-only root filesystem (where possible)
- Resource limits applied

## Monitoring and Health Checks

### Health Check Endpoints

```bash
# Basic health check
curl http://localhost:80/

# Expected response: JSON with server information
```

### Kubernetes Health Checks

The deployment includes:
- **Liveness Probe**: Ensures container is running
- **Readiness Probe**: Ensures container is ready to serve traffic

### Monitoring Integration

#### Prometheus Metrics (Example)
```yaml
# Add to deployment annotations
annotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "80"
  prometheus.io/path: "/"
```

#### Logging Integration
Configure structured logging for integration with log aggregation systems:

```yaml
echoServer:
  logs:
    format: "object"  # JSON format for log parsers
    level: "info"
```

## Troubleshooting

### Common Issues

#### Container Won't Start
```bash
# Check logs
docker logs echo-server
kubectl logs -n echo-server deployment/echo-server

# Check container status
docker ps -a
kubectl get pods -n echo-server
```

#### Port Binding Issues
```bash
# Check if port is already in use
lsof -i :80
netstat -tulpn | grep 80

# Use different port
docker run -p 8080:80 echo-server:latest
```

#### Permission Issues
```bash
# Ensure proper file permissions for volumes
chmod 755 /path/to/mounted/directory

# Check container user
docker exec echo-server id
```

#### Kubernetes Issues
```bash
# Check pod events
kubectl describe pod -n echo-server <pod-name>

# Check service endpoints
kubectl get endpoints -n echo-server

# Check ingress status
kubectl describe ingress -n echo-server echo-server-ingress
```

### Debug Mode

Enable debug logging:
```bash
# Docker
docker run -e LOGS__LEVEL=debug echo-server:latest

# Kubernetes
kubectl set env deployment/echo-server -n echo-server LOGS__LEVEL=debug

# Helm
helm upgrade my-echo-server ./helm/echo-server --set echoServer.logs.level=debug
```

### Performance Tuning

#### Resource Optimization
```yaml
# Kubernetes resources
resources:
  requests:
    memory: "32Mi"
    cpu: "50m"
  limits:
    memory: "128Mi"
    cpu: "200m"
```

#### Scaling Configuration
```yaml
# Horizontal Pod Autoscaler
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 20
  targetCPUUtilizationPercentage: 60
```

For more detailed troubleshooting, enable debug logging and check the application logs.
