---
layout: default
title: Feature Toggle
parent: Configuration
nav_order: 1
---

# Feature Toggle

Echo Server includes comprehensive feature toggles to control what information is included in responses and what functionality is available.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Response Content Features

### Enable Logs
**Environment Variable:** `ENABLE_LOGS`  
**Default:** `true`  
**CLI:** `--enable-logs` / `--disable-logs`

Controls whether the server generates and includes logs in the response.

```bash
# Disable logging
export ENABLE_LOGS=false

# Enable logging (default)
export ENABLE_LOGS=true
```

### Enable Host Information
**Environment Variable:** `ENABLE_HOST`  
**Default:** `true`  
**CLI:** `--enable-host` / `--disable-host`

Includes host information such as hostname, IP addresses, and OS details.

```bash
# Disable host info
export ENABLE_HOST=false
```

Response without host info:
```json
{
  "http": {...},
  "request": {...}
}
```

Response with host info:
```json
{
  "host": {
    "hostname": "echo-server-123",
    "ip": "10.244.0.5",
    "ips": ["10.244.0.5"],
    "os": {
      "hostname": "echo-server-123",
      "type": "Linux",
      "platform": "linux",
      "architecture": "x64"
    }
  },
  "http": {...},
  "request": {...}
}
```

### Enable HTTP Information
**Environment Variable:** `ENABLE_HTTP`  
**Default:** `true`  
**CLI:** `--enable-http` / `--disable-http`

Includes HTTP method, URL, and protocol information.

```bash
# Disable HTTP info
export ENABLE_HTTP=false
```

### Enable Request Details
**Environment Variable:** `ENABLE_REQUEST`  
**Default:** `true`  
**CLI:** `--enable-request` / `--disable-request`

Includes request parameters, query strings, headers, body, and files.

```bash
# Disable request details
export ENABLE_REQUEST=false
```

### Enable Cookies
**Environment Variable:** `ENABLE_COOKIES`  
**Default:** `true`  
**CLI:** `--enable-cookies` / `--disable-cookies`

Includes cookie information in the response.

```bash
# Disable cookies
export ENABLE_COOKIES=false
```

## Functional Features

### Enable File Operations
**Environment Variable:** `ENABLE_FILE`  
**Default:** `true`  
**CLI:** `--enable-file` / `--disable-file`

{: .warning }
**Security Warning**: File operations allow reading files and listing directories. Disable in production environments or untrusted networks.

Controls whether the `echo_file` parameter works for file and directory operations.

```bash
# Disable file operations (recommended for production)
export ENABLE_FILE=false
```

When disabled:
```bash
# This will return normal echo response instead of file content
curl http://localhost:80/?echo_file=/etc/passwd
```

When enabled:
```bash
# This will return file content or directory listing
curl http://localhost:80/?echo_file=/tmp
```

### Enable Custom Headers
**Environment Variable:** `ENABLE_HEADER`  
**Default:** `true`  
**CLI:** `--enable-header` / `--disable-header`

Controls whether custom headers can be added to responses via `echo_header`.

```bash
# Disable custom headers
export ENABLE_HEADER=false
```

### Enable Environment Variables
**Environment Variable:** `ENABLE_ENV`  
**Default:** `false`  
**CLI:** `--enable-env` / `--disable-env`

{: .warning }
**Security Warning**: Environment variables may contain sensitive information like API keys and passwords. Only enable in secure, trusted environments.

Controls whether environment variables are included in the response and whether `echo_env_body` parameter works.

```bash
# Enable environment variables (use with caution)
export ENABLE_ENV=true
```

When enabled, responses include:
```json
{
  "environment": {
    "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin",
    "HOME": "/home/user",
    "USER": "user"
  }
}
```

## Security Configurations

### Minimal Security Profile
For maximum security in production:

```bash
export ENABLE_FILE=false
export ENABLE_ENV=false
export ENABLE_COOKIES=false
export CONTROLS__TIMES__MAX=5000
```

### Development Profile
For development and testing:

```bash
export ENABLE_FILE=true
export ENABLE_ENV=true
export ENABLE_COOKIES=true
export LOGS__LEVEL=debug
```

### Public Demo Profile
For public demonstrations:

```bash
export ENABLE_FILE=false
export ENABLE_ENV=false
export ENABLE_COOKIES=true
export CONTROLS__TIMES__MAX=10000
```

## Docker Configuration

### Dockerfile Environment
```dockerfile
ENV ENABLE_FILE=false
ENV ENABLE_ENV=false
ENV ENABLE_LOGS=true
ENV ENABLE_HOST=true
ENV ENABLE_HTTP=true
ENV ENABLE_REQUEST=true
```

### Docker Run
```bash
docker run -p 80:80 \
  -e ENABLE_FILE=false \
  -e ENABLE_ENV=false \
  -e ENABLE_LOGS=true \
  echo-server:latest
```

### Docker Compose
```yaml
version: "3.8"
services:
  echo-server:
    image: echo-server:latest
    environment:
      - ENABLE_FILE=false
      - ENABLE_ENV=false
      - ENABLE_LOGS=true
      - ENABLE_HOST=true
      - ENABLE_HTTP=true
      - ENABLE_REQUEST=true
```

## Kubernetes Configuration

### ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: echo-server-config
data:
  ENABLE_FILE: "false"
  ENABLE_ENV: "false"
  ENABLE_LOGS: "true"
  ENABLE_HOST: "true"
  ENABLE_HTTP: "true"
  ENABLE_REQUEST: "true"
```

### Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: echo-server
        envFrom:
        - configMapRef:
            name: echo-server-config
```

## Helm Configuration

### Values File
```yaml
# values.yaml
echoServer:
  features:
    enableLogs: true
    enableHost: true
    enableHttp: true
    enableRequest: true
    enableCookies: true
    enableFile: false      # Disabled for security
    enableHeader: true
    enableEnv: false       # Disabled for security
```

### Override Values
```bash
helm install my-echo-server ./helm/echo-server \
  --set echoServer.features.enableFile=false \
  --set echoServer.features.enableEnv=false
```

## Runtime Changes

### Via Command Line
```bash
# Start with specific features
python run_server.py \
  --disable-file \
  --disable-env \
  --enable-logs
```

### Via Environment
```bash
# Change and restart
export ENABLE_FILE=false
python run_server.py
```

### Kubernetes Rolling Update
```bash
# Update ConfigMap
kubectl patch configmap echo-server-config -p '{"data":{"ENABLE_FILE":"false"}}'

# Restart deployment
kubectl rollout restart deployment/echo-server
```

## Validation

### Check Current Configuration
```bash
# Request with debug info shows current settings
curl http://localhost:80 | jq '.environment' | grep ENABLE
```

### Test Feature Toggles
```bash
# Test file operations (should fail if disabled)
curl http://localhost:80/?echo_file=/tmp

# Test environment variables (should fail if disabled)
curl http://localhost:80/?echo_env_body=PATH

# Test custom headers (should fail if disabled)
curl -I http://localhost:80/?echo_header=Custom:Value
```

## Best Practices

1. **Production Security**: Always disable `ENABLE_FILE` and `ENABLE_ENV` in production
2. **Development**: Enable all features for testing and debugging
3. **Public Demos**: Disable sensitive features but keep functional ones
4. **Monitoring**: Use `ENABLE_LOGS=true` for troubleshooting
5. **Performance**: Disable unnecessary features to reduce response size

## Common Issues

### File Operations Not Working
```bash
# Check if file operations are enabled
echo $ENABLE_FILE

# Enable file operations
export ENABLE_FILE=true
```

### Environment Variables Missing
```bash
# Check if environment variables are enabled
echo $ENABLE_ENV

# Enable environment variables (use with caution)
export ENABLE_ENV=true
```

### Custom Headers Ignored
```bash
# Check if custom headers are enabled
echo $ENABLE_HEADER

# Enable custom headers
export ENABLE_HEADER=true
```
