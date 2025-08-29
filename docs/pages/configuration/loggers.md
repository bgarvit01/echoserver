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
docker run -e LOGS__LEVEL=info echo-server:latest
```

## Log Formats

Echo Server supports three log formats optimized for different use cases.

### Default Format
**Environment Variable:** `LOGS__FORMAT=default`  
**Use Case:** Development and human-readable logs

```
2024-01-15 10:30:45 - echo-server - INFO - Server starting on 127.0.0.1:80
2024-01-15 10:30:45 - echo-server - INFO - All features enabled
2024-01-15 10:30:46 - echo-server - INFO - GET / - 200 - 1.23ms
```

### Line Format
**Environment Variable:** `LOGS__FORMAT=line`  
**Use Case:** Single-line logs for log aggregation systems

```
2024-01-15T10:30:45.123Z INFO echo-server Server starting on 127.0.0.1:80
2024-01-15T10:30:45.124Z INFO echo-server All features enabled
2024-01-15T10:30:46.456Z INFO echo-server GET / 200 1.23ms
```

### Object Format (JSON)
**Environment Variable:** `LOGS__FORMAT=object`  
**Use Case:** Structured logging for log analysis and monitoring systems

```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "INFO",
  "app": "echo-server",
  "message": "Server starting on 127.0.0.1:80",
  "host": "echo-server-pod-123",
  "pid": 1234
}
{
  "timestamp": "2024-01-15T10:30:46.456Z",
  "level": "INFO",
  "app": "echo-server",
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
export LOGS__APP=my-echo-server
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
export LOGS__APP=echo-server
```

Perfect for Elasticsearch, Logstash, and Kibana integration.

## Docker Configuration

### Basic Docker Logging
```bash
docker run -p 80:80 \
  -e LOGS__LEVEL=info \
  -e LOGS__FORMAT=line \
  echo-server:latest
```

### Docker Compose
```yaml
version: "3.8"
services:
  echo-server:
    image: echo-server:latest
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
  --log-opt tag="echo-server" \
  echo-server:latest
```

## Kubernetes Configuration

### ConfigMap for Logging
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: echo-server-logging-config
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
  name: echo-server
spec:
  template:
    spec:
      containers:
      - name: echo-server
        image: echo-server:latest
        envFrom:
        - configMapRef:
            name: echo-server-logging-config
```

### Viewing Logs
```bash
# View logs from all pods
kubectl logs -l app=echo-server

# Follow logs
kubectl logs -l app=echo-server -f

# View logs with timestamps
kubectl logs -l app=echo-server --timestamps=true

# View recent logs
kubectl logs -l app=echo-server --since=1h
```

## Helm Configuration

### Values File
```yaml
# values.yaml
echoServer:
  logs:
    level: "info"
    format: "object"
    app: "echo-helm"
```

### Template Usage
The Helm chart automatically configures logging:

```yaml
# templates/configmap.yaml
data:
  LOGS__LEVEL: {{ .Values.echoServer.logs.level | quote }}
  LOGS__FORMAT: {{ .Values.echoServer.logs.format | quote }}
  LOGS__APP: {{ .Values.echoServer.logs.app | quote }}
```

### Override Values
```bash
helm install my-echo-server ./helm/echo-server \
  --set echoServer.logs.level=debug \
  --set echoServer.logs.format=default
```

## Log Aggregation Integration

### Fluentd Configuration
```yaml
# fluentd.conf
<source>
  @type forward
  port 24224
</source>

<filter echo-server.**>
  @type parser
  key_name log
  format json
  reserve_data true
</filter>

<match echo-server.**>
  @type elasticsearch
  host elasticsearch.default.svc.cluster.local
  port 9200
  index_name echo-server-logs
</match>
```

### Filebeat Configuration
```yaml
# filebeat.yml
filebeat.inputs:
- type: container
  paths:
    - '/var/log/containers/echo-server-*.log'
  json.keys_under_root: true
  json.add_error_key: true

output.elasticsearch:
  hosts: ["elasticsearch:9200"]
  index: "echo-server-logs-%{+yyyy.MM.dd}"
```

### Promtail Configuration (Loki)
```yaml
# promtail.yml
server:
  http_listen_port: 9080

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
- job_name: echo-server
  static_configs:
  - targets:
      - localhost
    labels:
      job: echo-server
      __path__: /var/log/echo-server/*.log
  pipeline_stages:
  - json:
      expressions:
        level: level
        message: message
        timestamp: timestamp
```

## Monitoring Integration

### Prometheus Metrics from Logs
With structured logging (object format), you can extract metrics:

```bash
# Count log levels
jq -r '.level' logs.json | sort | uniq -c

# Average response time
jq -r 'select(.duration) | .duration' logs.json | awk '{sum+=$1; n++} END {print sum/n}'

# Top endpoints
jq -r 'select(.path) | .path' logs.json | sort | uniq -c | sort -nr
```

### Grafana Log Panels
Query examples for Grafana with Loki:

```promql
# Error rate
rate({app="echo-server"} |= "ERROR" [5m])

# Response time percentiles
quantile_over_time(0.95, {app="echo-server"} | json | duration [5m])

# Request volume
sum(rate({app="echo-server"} | json | __error__="" [5m])) by (method)
```

## Performance Considerations

### Log Level Impact
- **Debug**: High overhead, detailed information
- **Info**: Moderate overhead, operational information
- **Warning**: Low overhead, important events only
- **Error**: Minimal overhead, errors only

### Format Performance
- **Default**: Fastest for human reading
- **Line**: Good balance of speed and structure
- **Object**: Higher overhead but better for analysis

### Production Recommendations
```bash
# Optimal production settings
export LOGS__LEVEL=info
export LOGS__FORMAT=object
export LOGS__APP=echo-prod
```

## Troubleshooting

### Log Level Not Working
```bash
# Check current log level
echo $LOGS__LEVEL

# Verify with command line override
python run_server.py --log-level debug
```

### Log Format Issues
```bash
# Check current format
echo $LOGS__FORMAT

# Test different formats
python run_server.py --log-format object
```

### Missing Logs in Kubernetes
```bash
# Check if logging is enabled
kubectl get configmap echo-server-config -o yaml | grep LOGS

# Check pod logs
kubectl logs deployment/echo-server

# Check log forwarding
kubectl get pods -l app=echo-server
```

### Docker Log Issues
```bash
# Check Docker logs
docker logs container-name

# Check log driver
docker inspect container-name | grep LogConfig

# Test with different log driver
docker run --log-driver=json-file echo-server:latest
```

## Best Practices

1. **Production**: Use `info` level with `object` format
2. **Development**: Use `debug` level with `default` format  
3. **Log Aggregation**: Use `object` format for structured data
4. **Performance**: Use higher log levels in high-traffic environments
5. **Monitoring**: Include structured fields for metrics extraction
6. **Security**: Avoid logging sensitive information
7. **Retention**: Configure appropriate log retention policies
