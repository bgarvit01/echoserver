---
layout: page
title: Kubernetes Deployment
permalink: /kubernetes/
---

# Kubernetes Deployment

Deploy Echo Server on Kubernetes for production-ready orchestration.

## Quick Deployment

### All-in-One Deployment
```bash
# Deploy everything
kubectl apply -f https://raw.githubusercontent.com/bgarvit01/echoserver/main/k8s/echo-server-all.yaml

# Port forward for testing
kubectl port-forward -n echoserver service/echoserver 80:80

# Test the service
curl http://localhost:80
```

## Manual Deployment

### Create Namespace
```bash
kubectl apply -f k8s/namespace.yaml
```

### Create ConfigMap
```bash
kubectl apply -f k8s/configmap.yaml
```

### Create Deployment
```bash
kubectl apply -f k8s/deployment.yaml
```

### Create Service
```bash
kubectl apply -f k8s/service.yaml
```

### Create Ingress (Optional)
```bash
kubectl apply -f k8s/ingress.yaml
```

## Configuration Examples

### Basic Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: echoserver
  namespace: echoserver
spec:
  replicas: 5
  selector:
    matchLabels:
      app: echoserver
  template:
    metadata:
      labels:
        app: echoserver
    spec:
      containers:
      - name: echoserver
        image: echoserver:latest
        ports:
        - containerPort: 80
        env:
        - name: LOGS__LEVEL
          value: "info"
        - name: ENABLE_FILE
          value: "false"
        - name: ENABLE_ENV
          value: "false"
```

### ConfigMap for Environment Variables
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: echoserver-config
  namespace: echoserver
data:
  LOGS__LEVEL: "info"
  LOGS__FORMAT: "object"
  ENABLE_FILE: "false"
  ENABLE_ENV: "false"
  ENABLE_LOGS: "true"
```

### Service Configuration
```yaml
apiVersion: v1
kind: Service
metadata:
  name: echoserver
  namespace: echoserver
spec:
  selector:
    app: echoserver
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP
```

## Monitoring

### Check Deployment Status
```bash
kubectl get deployments -n echoserver
kubectl get pods -n echoserver
kubectl get services -n echoserver
```

### View Logs
```bash
# All pods
kubectl logs -n echoserver -l app=echoserver

# Specific pod
kubectl logs -n echoserver <pod-name>

# Follow logs
kubectl logs -n echoserver -l app=echoserver -f
```

## Scaling

```bash
# Scale up
kubectl scale deployment/echoserver -n echoserver --replicas=10

# Scale down
kubectl scale deployment/echoserver -n echoserver --replicas=3
```

## Updating Configuration

```bash
# Update ConfigMap
kubectl edit configmap echoserver-config -n echoserver

# Restart deployment to pick up changes
kubectl rollout restart deployment/echoserver -n echoserver

# Check rollout status
kubectl rollout status deployment/echoserver -n echoserver
```

## Cleanup

```bash
# Delete specific resources
kubectl delete -f k8s/deployment.yaml
kubectl delete -f k8s/service.yaml
kubectl delete -f k8s/configmap.yaml
kubectl delete -f k8s/namespace.yaml

# Or delete everything at once
kubectl delete namespace echoserver
```

