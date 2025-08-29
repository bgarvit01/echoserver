---
layout: default
title: Kubernetes
parent: Quick Start
nav_order: 3
---

# Kubernetes

Deploy Echo Server on Kubernetes for production-ready orchestration.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Quick Deploy

### One-Command Deployment
```bash
# Deploy everything at once
kubectl apply -f https://raw.githubusercontent.com/yourusername/echoserver/main/k8s/echo-server-all.yaml

# Or download and customize
wget https://raw.githubusercontent.com/yourusername/echoserver/main/k8s/echo-server-all.yaml
kubectl apply -f echo-server-all.yaml
```

This deployment includes:
- **Namespace** creation
- **ConfigMap** with configuration
- **Deployment** with 5 replicas
- **Service** for internal access
- **Ingress** for external access

## Step by Step Deployment

### Deploy Individual Components
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

## Access the Service

### Port Forward for Testing
```bash
# Forward port for local testing
kubectl port-forward -n echo-server service/echo-server-service 80:80

# Test the service
curl http://localhost:80
```

### Via Ingress
```bash
# Add to /etc/hosts (replace <ingress-ip> with actual IP)
echo "<ingress-ip> echo.local" | sudo tee -a /etc/hosts

# Access via domain
curl http://echo.local
```

### Via NodePort (Alternative)
```bash
# Change service type to NodePort
kubectl patch service echo-server-service -n echo-server -p '{"spec":{"type":"NodePort"}}'

# Get the node port
kubectl get service echo-server-service -n echo-server

# Access via NodePort
curl http://<node-ip>:<node-port>
```

## Configuration

### Environment Variables
The deployment uses a ConfigMap for configuration:

```yaml
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: echo-server-config
  namespace: echo-server
data:
  LOGS__LEVEL: "info"
  LOGS__FORMAT: "default"
  ENABLE_LOGS: "true"
  ENABLE_HOST: "true"
  ENABLE_HTTP: "true"
  ENABLE_REQUEST: "true"
  ENABLE_FILE: "false"
  ENABLE_ENV: "false"
  CONTROLS__TIMES__MAX: "30000"
```

### Update Configuration
```bash
# Edit the ConfigMap
kubectl edit configmap echo-server-config -n echo-server

# Restart deployment to pick up changes
kubectl rollout restart deployment/echo-server -n echo-server

# Check rollout status
kubectl rollout status deployment/echo-server -n echo-server
```

## Scaling

### Manual Scaling
```bash
# Scale to 10 replicas
kubectl scale deployment echo-server -n echo-server --replicas=10

# Check scaling status
kubectl get deployment echo-server -n echo-server

# Watch pods scaling
kubectl get pods -n echo-server -w
```

### Horizontal Pod Autoscaler
```bash
# Create HPA (requires metrics-server)
kubectl autoscale deployment echo-server -n echo-server \
  --cpu-percent=70 \
  --min=2 \
  --max=20

# Check HPA status
kubectl get hpa -n echo-server

# View HPA details
kubectl describe hpa echo-server -n echo-server
```

## Monitoring

### View Deployment Status
```bash
# Check all resources
kubectl get all -n echo-server

# Check deployment status
kubectl get deployment echo-server -n echo-server -o wide

# Check pod status
kubectl get pods -n echo-server

# Check service endpoints
kubectl get endpoints -n echo-server
```

### View Logs
```bash
# View logs from all pods
kubectl logs -n echo-server deployment/echo-server

# Follow logs
kubectl logs -n echo-server deployment/echo-server -f

# View logs from specific pod
kubectl logs -n echo-server <pod-name>

# View previous container logs
kubectl logs -n echo-server <pod-name> --previous
```

### Debugging
```bash
# Describe deployment
kubectl describe deployment echo-server -n echo-server

# Describe pod
kubectl describe pod <pod-name> -n echo-server

# Execute commands in pod
kubectl exec -it <pod-name> -n echo-server -- /bin/bash

# Check pod events
kubectl get events -n echo-server --sort-by='.lastTimestamp'
```

## Examples

### Test Basic Functionality
```bash
# Port forward
kubectl port-forward -n echo-server service/echo-server-service 80:80 &

# Test basic echo
curl http://localhost:80

# Test custom status code
curl -I http://localhost:80/?echo_code=404

# Test custom body
curl http://localhost:80/?echo_body=hello

# Test custom headers
curl -I http://localhost:80/?echo_header=Custom:Value
```

### Load Testing
```bash
# Install hey (load testing tool)
# brew install hey  # macOS
# apt-get install hey  # Ubuntu

# Run load test
hey -n 1000 -c 10 http://localhost:80

# Test with custom query
hey -n 1000 -c 10 "http://localhost:80/?echo_body=load-test"
```

## Production Configuration

### Resource Limits
The deployment includes production-ready resource limits:

```yaml
resources:
  requests:
    memory: "64Mi"
    cpu: "100m"
  limits:
    memory: "128Mi"
    cpu: "200m"
```

### Security Context
Security features enabled:

```yaml
securityContext:
  allowPrivilegeEscalation: false
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: false
  capabilities:
    drop:
    - ALL
```

### Health Checks
Liveness and readiness probes configured:

```yaml
livenessProbe:
  httpGet:
    path: /
    port: 80
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /
    port: 80
  initialDelaySeconds: 5
  periodSeconds: 5
```

## Ingress Controller

### NGINX Ingress
The deployment is configured for NGINX Ingress Controller:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/rewrite-target: /
```

### Install NGINX Ingress Controller
```bash
# Install NGINX Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml

# Wait for controller to be ready
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s
```

## Troubleshooting

### Pod Issues
```bash
# Check if pods are running
kubectl get pods -n echo-server

# Check pod events
kubectl describe pod <pod-name> -n echo-server

# Check pod logs
kubectl logs <pod-name> -n echo-server
```

### Service Issues
```bash
# Check service
kubectl get service echo-server-service -n echo-server

# Check endpoints
kubectl get endpoints echo-server-service -n echo-server

# Test service from within cluster
kubectl run test-pod --image=curlimages/curl -it --rm -- \
  curl echo-server-service.echo-server.svc.cluster.local
```

### Ingress Issues
```bash
# Check ingress
kubectl get ingress -n echo-server

# Describe ingress
kubectl describe ingress echo-server-ingress -n echo-server

# Check ingress controller logs
kubectl logs -n ingress-nginx deployment/ingress-nginx-controller
```

### Common Solutions
```bash
# Restart deployment
kubectl rollout restart deployment/echo-server -n echo-server

# Delete and recreate pod
kubectl delete pod <pod-name> -n echo-server

# Clean up and redeploy
kubectl delete namespace echo-server
kubectl apply -f k8s/echo-server-all.yaml
```
