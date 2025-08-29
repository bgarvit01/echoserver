---
layout: default
title: Helm
parent: Quick Start
nav_order: 4
---

# Helm

Deploy Echo Server using Helm for Kubernetes package management.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Prerequisites

- Helm 3.0+
- Kubernetes cluster access
- kubectl configured

## Installation

### Install from Local Chart

#### Basic Installation
```bash
# Install with default values
helm install my-echo-server ./helm/echo-server

# Install in specific namespace
helm install my-echo-server ./helm/echo-server \
  --namespace echo-server \
  --create-namespace
```

#### Custom Installation
```bash
# Install with custom values
helm install my-echo-server ./helm/echo-server \
  --set replicaCount=5 \
  --set echoServer.logs.level=info \
  --set ingress.enabled=true
```

### Install with Values File

#### Production Values
```bash
# Use production configuration
helm install my-echo-server ./helm/echo-server \
  -f examples/production-values.yaml
```

#### Development Values
```bash
# Use development configuration
helm install my-echo-server ./helm/echo-server \
  -f examples/development-values.yaml
```

## Configuration

### Default Values

The chart includes comprehensive default values:

```yaml
replicaCount: 5

image:
  repository: echo-server
  pullPolicy: IfNotPresent
  tag: "latest"

service:
  type: ClusterIP
  port: 80
  targetPort: 80

ingress:
  enabled: false
  className: "nginx"

echoServer:
  logs:
    level: "info"
    format: "default"
  features:
    enableLogs: true
    enableHost: true
    enableHttp: true
    enableRequest: true
    enableFile: false
    enableEnv: false
```

### Custom Values Examples

#### Production Configuration
```yaml
# values-production.yaml
replicaCount: 5

ingress:
  enabled: true
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

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

#### Development Configuration
```yaml
# values-development.yaml
replicaCount: 1

service:
  type: NodePort

echoServer:
  logs:
    level: "debug"
    format: "default"
  features:
    enableFile: true
    enableEnv: true

resources:
  limits:
    cpu: 200m
    memory: 128Mi
```

## Management

### List Installations
```bash
# List all releases
helm list

# List releases in specific namespace
helm list -n echo-server

# List all releases across namespaces
helm list --all-namespaces
```

### Check Status
```bash
# Get release status
helm status my-echo-server

# Get release values
helm get values my-echo-server

# Get release manifest
helm get manifest my-echo-server
```

### Upgrade
```bash
# Upgrade with new values
helm upgrade my-echo-server ./helm/echo-server \
  --set replicaCount=10

# Upgrade with values file
helm upgrade my-echo-server ./helm/echo-server \
  -f values-production.yaml

# Upgrade and wait for rollout
helm upgrade my-echo-server ./helm/echo-server \
  --wait --timeout=300s
```

### Rollback
```bash
# List release history
helm history my-echo-server

# Rollback to previous version
helm rollback my-echo-server

# Rollback to specific revision
helm rollback my-echo-server 1
```

### Uninstall
```bash
# Uninstall release
helm uninstall my-echo-server

# Uninstall and remove namespace
helm uninstall my-echo-server -n echo-server
kubectl delete namespace echo-server
```

## Examples

### Basic Deployment
```bash
# Install Echo Server
helm install echo ./helm/echo-server

# Check deployment
kubectl get pods -l app.kubernetes.io/instance=echo

# Port forward for testing
kubectl port-forward service/echo-echo-server 80:80

# Test the service
curl http://localhost:80
```

### Production Deployment
```bash
# Install with production values
helm install echo-prod ./helm/echo-server \
  -f examples/production-values.yaml \
  --namespace production \
  --create-namespace

# Check status
helm status echo-prod -n production

# View all resources
kubectl get all -n production -l app.kubernetes.io/instance=echo-prod
```

### Development Environment
```bash
# Install development environment
helm install echo-dev ./helm/echo-server \
  -f examples/development-values.yaml \
  --namespace development \
  --create-namespace

# Enable debug logging
helm upgrade echo-dev ./helm/echo-server \
  --reuse-values \
  --set echoServer.logs.level=debug
```

## Advanced Configuration

### Autoscaling
```bash
# Enable autoscaling
helm upgrade my-echo-server ./helm/echo-server \
  --set autoscaling.enabled=true \
  --set autoscaling.minReplicas=2 \
  --set autoscaling.maxReplicas=20 \
  --set autoscaling.targetCPUUtilizationPercentage=60
```

### Ingress with TLS
```bash
# Enable ingress with TLS
helm upgrade my-echo-server ./helm/echo-server \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host=echo.example.com \
  --set ingress.hosts[0].paths[0].path=/ \
  --set ingress.hosts[0].paths[0].pathType=Prefix \
  --set ingress.tls[0].secretName=echo-tls \
  --set ingress.tls[0].hosts[0]=echo.example.com
```

### Resource Limits
```bash
# Set resource limits
helm upgrade my-echo-server ./helm/echo-server \
  --set resources.limits.cpu=500m \
  --set resources.limits.memory=256Mi \
  --set resources.requests.cpu=100m \
  --set resources.requests.memory=128Mi
```

## Helm Repository (Optional)

### Add Repository
```bash
# Add Echo Server Helm repository (replace with actual repo)
helm repo add echo-server https://bgarvit01.github.io/echoserver/

# Update repository
helm repo update

# Search for charts
helm search repo echo-server
```

### Install from Repository
```bash
# Install from repository
helm install my-echo-server echo-server/echo-server

# Install specific version
helm install my-echo-server echo-server/echo-server --version 1.0.0
```

## Troubleshooting

### Chart Issues
```bash
# Validate chart
helm lint ./helm/echo-server

# Debug template rendering
helm template test-release ./helm/echo-server --debug

# Dry run installation
helm install my-echo-server ./helm/echo-server --dry-run --debug
```

### Release Issues
```bash
# Check release notes
helm get notes my-echo-server

# Check release history
helm history my-echo-server

# Get all release information
helm get all my-echo-server
```

### Pod Issues
```bash
# Get pods for release
kubectl get pods -l app.kubernetes.io/instance=my-echo-server

# Check pod logs
kubectl logs -l app.kubernetes.io/instance=my-echo-server

# Describe deployment
kubectl describe deployment -l app.kubernetes.io/instance=my-echo-server
```

### Common Solutions
```bash
# Force upgrade
helm upgrade my-echo-server ./helm/echo-server --force

# Reset values to defaults
helm upgrade my-echo-server ./helm/echo-server --reset-values

# Clean reinstall
helm uninstall my-echo-server
helm install my-echo-server ./helm/echo-server
```

## Best Practices

### Version Management
```bash
# Always specify chart version in production
helm install my-echo-server ./helm/echo-server --version 1.0.0

# Pin image tag
helm install my-echo-server ./helm/echo-server \
  --set image.tag=v1.0.0
```

### Values Management
```bash
# Use separate values files for environments
helm install echo-prod ./helm/echo-server -f values-production.yaml
helm install echo-dev ./helm/echo-server -f values-development.yaml

# Use --reuse-values for minor updates
helm upgrade my-echo-server ./helm/echo-server \
  --reuse-values \
  --set replicaCount=10
```

### Security
```bash
# Always create dedicated namespace
helm install my-echo-server ./helm/echo-server \
  --namespace echo-server \
  --create-namespace

# Use RBAC and service accounts
helm install my-echo-server ./helm/echo-server \
  --set serviceAccount.create=true
```
