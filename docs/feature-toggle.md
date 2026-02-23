---
layout: page
title: Feature-Toggle
nav_order: 7
permalink: /feature-toggle/
parent: Configuration
---

# Feature-Toggle

Control what information is included in responses and what functionality is available.

---

## Response Content Features

### Enable Logs

**Variable:** `ENABLE_LOGS`  
**Default:** `true`

Controls whether the server generates and includes logs.

```bash
export ENABLE_LOGS=false
```

### Enable Host Information

**Variable:** `ENABLE_HOST`  
**Default:** `true`

Includes hostname, IP addresses, and OS details.

```bash
export ENABLE_HOST=false
```

Response with host info:
```json
{
  "host": {
    "hostname": "echoserver-123",
    "ip": "10.244.0.5",
    "ips": ["10.244.0.5"]
  }
}
```

### Enable HTTP Information

**Variable:** `ENABLE_HTTP`  
**Default:** `true`

Includes HTTP method, URL, and protocol.

```bash
export ENABLE_HTTP=false
```

### Enable Request Details

**Variable:** `ENABLE_REQUEST`  
**Default:** `true`

Includes parameters, query strings, headers, body, and files.

```bash
export ENABLE_REQUEST=false
```

### Enable Cookies

**Variable:** `ENABLE_COOKIES`  
**Default:** `true`

Includes cookie information.

```bash
export ENABLE_COOKIES=false
```

---

## Functional Features

### Enable File Operations

**Variable:** `ENABLE_FILE`  
**Default:** `true`

⚠️ **Security Warning**: File operations allow reading files and listing directories. Disable in production.

```bash
export ENABLE_FILE=false
```

When enabled:
```bash
curl http://localhost:80/?echo_file=/tmp
```

### Enable Custom Headers

**Variable:** `ENABLE_HEADER`  
**Default:** `true`

Controls custom headers via `echo_header`.

```bash
export ENABLE_HEADER=false
```

### Enable Environment Variables

**Variable:** `ENABLE_ENV`  
**Default:** `false`

⚠️ **Security Warning**: Environment variables may contain sensitive information. Only enable in secure environments.

```bash
export ENABLE_ENV=true
```

When enabled:
```json
{
  "environment": {
    "PATH": "/usr/local/bin:/usr/bin",
    "HOME": "/home/user"
  }
}
```

---

## Security Profiles

### Minimal Security (Production)

```bash
export ENABLE_FILE=false
export ENABLE_ENV=false
export ENABLE_COOKIES=false
export CONTROLS__TIMES__MAX=5000
```

### Development

```bash
export ENABLE_FILE=true
export ENABLE_ENV=true
export ENABLE_COOKIES=true
export LOGS__LEVEL=debug
```

### Public Demo

```bash
export ENABLE_FILE=false
export ENABLE_ENV=false
export ENABLE_COOKIES=true
export CONTROLS__TIMES__MAX=10000
```

---

## Docker Configuration

```bash
docker run -p 80:80 \
  -e ENABLE_FILE=false \
  -e ENABLE_ENV=false \
  -e ENABLE_LOGS=true \
  echoserver:latest
```

## Kubernetes Configuration

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: echoserver-config
data:
  ENABLE_FILE: "false"
  ENABLE_ENV: "false"
  ENABLE_LOGS: "true"
```

---

**Related:** [Configuration →]({{ site.baseurl }}/configuration/)
