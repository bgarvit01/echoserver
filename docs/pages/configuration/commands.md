---
layout: default
title: Commands
parent: Configuration
nav_order: 3
---

# Commands

Echo Server allows customization of command names and parameters for maximum flexibility in different environments.

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Default Commands

Echo Server responds to these default commands via query parameters or HTTP headers:

| Function | Query Parameter | HTTP Header | Description |
|----------|----------------|-------------|-------------|
| Custom Body | `echo_body` | `x-echo-body` | Set custom response body |
| Environment Body | `echo_env_body` | `x-echo-env-body` | Use environment variable as body |
| Status Code | `echo_code` | `x-echo-code` | Set HTTP status code |
| Custom Headers | `echo_header` | `x-echo-header` | Add custom response headers |
| Response Delay | `echo_time` | `x-echo-time` | Add response delay in milliseconds |
| File Operations | `echo_file` | `x-echo-file` | Read file or list directory |

## Command Customization

All command names can be customized using environment variables:

### Custom Body Commands
```bash
# Change query parameter name
export COMMANDS__HTTPBODY__QUERY=custom_body

# Change header name  
export COMMANDS__HTTPBODY__HEADER=x-custom-body

# Usage with custom names
curl http://localhost:80/?custom_body=hello
curl -H "X-Custom-Body: world" http://localhost:80
```

### Environment Body Commands
```bash
export COMMANDS__HTTPENVBODY__QUERY=env_response
export COMMANDS__HTTPENVBODY__HEADER=x-env-response

# Usage
curl http://localhost:80/?env_response=HOSTNAME
curl -H "X-Env-Response: USER" http://localhost:80
```

### Status Code Commands
```bash
export COMMANDS__HTTPCODE__QUERY=status
export COMMANDS__HTTPCODE__HEADER=x-status

# Usage
curl -I http://localhost:80/?status=404
curl -I -H "X-Status: 500" http://localhost:80
```

### Custom Headers Commands
```bash
export COMMANDS__HTTPHEADERS__QUERY=headers
export COMMANDS__HTTPHEADERS__HEADER=x-headers

# Usage
curl -I http://localhost:80/?headers=Custom:Value
curl -I -H "X-Headers: Custom:Value" http://localhost:80
```

### Response Delay Commands
```bash
export COMMANDS__TIME__QUERY=delay
export COMMANDS__TIME__HEADER=x-delay

# Usage
curl http://localhost:80/?delay=2000
curl -H "X-Delay: 3000" http://localhost:80
```

### File Operations Commands
```bash
export COMMANDS__FILE__QUERY=file
export COMMANDS__FILE__HEADER=x-file

# Usage
curl http://localhost:80/?file=/tmp
curl -H "X-File: /etc/hostname" http://localhost:80
```

## Complete Command Customization Example

```bash
# API-style naming
export COMMANDS__HTTPBODY__QUERY=response_body
export COMMANDS__HTTPBODY__HEADER=x-api-response-body
export COMMANDS__HTTPCODE__QUERY=response_code
export COMMANDS__HTTPCODE__HEADER=x-api-response-code
export COMMANDS__HTTPHEADERS__QUERY=response_headers
export COMMANDS__HTTPHEADERS__HEADER=x-api-response-headers
export COMMANDS__TIME__QUERY=response_delay
export COMMANDS__TIME__HEADER=x-api-response-delay
export COMMANDS__FILE__QUERY=file_content
export COMMANDS__FILE__HEADER=x-api-file-content
export COMMANDS__HTTPENVBODY__QUERY=env_var
export COMMANDS__HTTPENVBODY__HEADER=x-api-env-var

# Usage with custom API-style commands
curl http://localhost:80/?response_body=hello&response_code=201
curl -H "X-Api-Response-Body: success" -H "X-Api-Response-Code: 200" http://localhost:80
```

## Docker Configuration

### Dockerfile
```dockerfile
ENV COMMANDS__HTTPBODY__QUERY=custom_body
ENV COMMANDS__HTTPBODY__HEADER=x-custom-body
ENV COMMANDS__HTTPCODE__QUERY=status_code
ENV COMMANDS__HTTPCODE__HEADER=x-status-code
```

### Docker Run
```bash
docker run -p 80:80 \
  -e COMMANDS__HTTPBODY__QUERY=response \
  -e COMMANDS__HTTPBODY__HEADER=x-response \
  -e COMMANDS__HTTPCODE__QUERY=code \
  -e COMMANDS__HTTPCODE__HEADER=x-code \
  echo-server:latest
```

### Docker Compose
```yaml
version: "3.8"
services:
  echo-server:
    image: echo-server:latest
    environment:
      - COMMANDS__HTTPBODY__QUERY=body
      - COMMANDS__HTTPBODY__HEADER=x-body
      - COMMANDS__HTTPCODE__QUERY=status
      - COMMANDS__HTTPCODE__HEADER=x-status
      - COMMANDS__TIME__QUERY=delay
      - COMMANDS__TIME__HEADER=x-delay
```

## Kubernetes Configuration

### ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: echo-server-commands
data:
  COMMANDS__HTTPBODY__QUERY: "response_body"
  COMMANDS__HTTPBODY__HEADER: "x-response-body"
  COMMANDS__HTTPCODE__QUERY: "response_code"
  COMMANDS__HTTPCODE__HEADER: "x-response-code"
  COMMANDS__HTTPHEADERS__QUERY: "response_headers"
  COMMANDS__HTTPHEADERS__HEADER: "x-response-headers"
  COMMANDS__TIME__QUERY: "response_delay"
  COMMANDS__TIME__HEADER: "x-response-delay"
  COMMANDS__FILE__QUERY: "file_content"
  COMMANDS__FILE__HEADER: "x-file-content"
  COMMANDS__HTTPENVBODY__QUERY: "env_variable"
  COMMANDS__HTTPENVBODY__HEADER: "x-env-variable"
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
            name: echo-server-commands
```

### Update Commands at Runtime
```bash
# Update ConfigMap
kubectl patch configmap echo-server-commands -p '{"data":{"COMMANDS__HTTPBODY__QUERY":"new_body"}}'

# Restart deployment to pick up changes
kubectl rollout restart deployment/echo-server
```

