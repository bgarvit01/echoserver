---
layout: page
title: Feature Toggles
permalink: /feature-toggle/
---

# Feature Toggles

Echo Server includes comprehensive feature toggles to control what information is included in responses and what functionality is available.

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

Response with host info:
```json
{
  "host": {
    "hostname": "echoserver-123",
    "ip": "10.244.0.5",
    "ips": ["10.244.0.5"],
    "os": {
      "hostname": "echoserver-123",
      "type": "Linux",
      "platform": "linux",
      "architecture": "x64"
    }
  }
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

> **Security Warning**: File operations allow reading files and listing directories. Disable in production environments or untrusted networks.

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

> **Security Warning**: Environment variables may contain sensitive information like API keys and passwords. Only enable in secure, trusted environments.

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

### Docker Run
```bash
docker run -p 80:80 \
  -e ENABLE_FILE=false \
  -e ENABLE_ENV=false \
  -e ENABLE_LOGS=true \
  echoserver:latest
```

### Docker Compose
```yaml
version: "3.8"
services:
  echoserver:
    image: echoserver:latest
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
  name: echoserver-config
data:
  ENABLE_FILE: "false"
  ENABLE_ENV: "false"
  ENABLE_LOGS: "true"
  ENABLE_HOST: "true"
  ENABLE_HTTP: "true"
  ENABLE_REQUEST: "true"
```

