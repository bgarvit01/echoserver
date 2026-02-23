---
layout: page
title: Kubernetes
nav_order: 5
permalink: /kubernetes/
parent: Quick-Start
---

# Kubernetes

## Quick Deployment

Deploy everything with one command:

```bash
# Deploy
kubectl apply -f https://raw.githubusercontent.com/bgarvit01/echoserver/main/k8s/echoserver-all.yaml

# Port forward for testing
kubectl port-forward -n echoserver service/echoserver 80:80

# Test
curl http://localhost:80
```

## Manual Deployment

### 1. Create Namespace

```bash
kubectl create namespace echoserver
```

### 2. Create ConfigMap

`configmap.yaml`:

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
```

```bash
kubectl apply -f configmap.yaml
```

### 3. Create Deployment

`deployment.yaml`:

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
        envFrom:
        - configMapRef:
            name: echoserver-config
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "500m"
```

```bash
kubectl apply -f deployment.yaml
```

### 4. Create Service

`service.yaml`:

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

```bash
kubectl apply -f service.yaml
```

### 5. Create Ingress (Optional)

`ingress.yaml`:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: echoserver
  namespace: echoserver
spec:
  rules:
  - host: echo.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: echoserver
            port:
              number: 80
```

```bash
kubectl apply -f ingress.yaml
```

## Monitoring

```bash
# Check deployment status
kubectl get deployments -n echoserver

# Check pods
kubectl get pods -n echoserver

# Check service
kubectl get services -n echoserver

# View logs
kubectl logs -n echoserver -l app=echoserver -f

# Describe pod
kubectl describe pod -n echoserver <pod-name>
```

## Scaling

```bash
# Scale up
kubectl scale deployment/echoserver -n echoserver --replicas=10

# Scale down
kubectl scale deployment/echoserver -n echoserver --replicas=3

# Autoscale
kubectl autoscale deployment echoserver -n echoserver --min=3 --max=10 --cpu-percent=80
```

## Update Configuration

```bash
# Edit ConfigMap
kubectl edit configmap echoserver-config -n echoserver

# Restart deployment to apply changes
kubectl rollout restart deployment/echoserver -n echoserver

# Check rollout status
kubectl rollout status deployment/echoserver -n echoserver
```

## Cleanup

```bash
# Delete specific resources
kubectl delete deployment echoserver -n echoserver
kubectl delete service echoserver -n echoserver
kubectl delete configmap echoserver-config -n echoserver

# Or delete entire namespace
kubectl delete namespace echoserver
```

---

**Next:** [Configuration →]({{ site.baseurl }}/configuration/)
