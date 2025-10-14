---
layout: page
title: Commands
nav_order: 8
permalink: /commands/
parent: Configuration
---

# Commands

Customize command names and parameters for maximum flexibility.

---

## Default Commands

| Function | Query Parameter | HTTP Header | Description |
|----------|----------------|-------------|-------------|
| Custom Body | `echo_body` | `x-echo-body` | Set custom response body |
| Environment Body | `echo_env_body` | `x-echo-env-body` | Use environment variable as body |
| Status Code | `echo_code` | `x-echo-code` | Set HTTP status code |
| Custom Headers | `echo_header` | `x-echo-header` | Add custom response headers |
| Response Delay | `echo_time` | `x-echo-time` | Add response delay (milliseconds) |
| File Operations | `echo_file` | `x-echo-file` | Read file or list directory |

### Usage Examples

```bash
# Custom body
curl http://localhost:80/?echo_body=hello

# Custom status code
curl -I http://localhost:80/?echo_code=404

# Custom header
curl -I http://localhost:80/?echo_header=Custom:Value

# Response delay (2 seconds)
curl http://localhost:80/?echo_time=2000

# File operations
curl http://localhost:80/?echo_file=/tmp

# Environment variable as body
curl http://localhost:80/?echo_env_body=HOSTNAME
```

---

## Customization

All command names can be customized using environment variables.

### Custom Body

```bash
export COMMANDS__HTTPBODY__QUERY=custom_body
export COMMANDS__HTTPBODY__HEADER=x-custom-body

# Usage
curl http://localhost:80/?custom_body=hello
curl -H "X-Custom-Body: world" http://localhost:80
```

### Status Code

```bash
export COMMANDS__HTTPCODE__QUERY=status
export COMMANDS__HTTPCODE__HEADER=x-status

# Usage
curl -I http://localhost:80/?status=404
curl -I -H "X-Status: 500" http://localhost:80
```

### Custom Headers

```bash
export COMMANDS__HTTPHEADERS__QUERY=headers
export COMMANDS__HTTPHEADERS__HEADER=x-headers

# Usage
curl -I http://localhost:80/?headers=Custom:Value
```

### Response Delay

```bash
export COMMANDS__TIME__QUERY=delay
export COMMANDS__TIME__HEADER=x-delay

# Usage
curl http://localhost:80/?delay=2000
```

### File Operations

```bash
export COMMANDS__FILE__QUERY=file
export COMMANDS__FILE__HEADER=x-file

# Usage
curl http://localhost:80/?file=/tmp
```

### Environment Body

```bash
export COMMANDS__HTTPENVBODY__QUERY=env_response
export COMMANDS__HTTPENVBODY__HEADER=x-env-response

# Usage
curl http://localhost:80/?env_response=HOSTNAME
```

---

## Examples

### API-Style Naming

```bash
export COMMANDS__HTTPBODY__QUERY=response_body
export COMMANDS__HTTPBODY__HEADER=x-api-response-body
export COMMANDS__HTTPCODE__QUERY=response_code
export COMMANDS__HTTPCODE__HEADER=x-api-response-code
export COMMANDS__TIME__QUERY=response_delay
export COMMANDS__TIME__HEADER=x-api-response-delay

# Usage
curl http://localhost:80/?response_body=hello&response_code=201
curl -H "X-Api-Response-Body: success" http://localhost:80
```

### Docker

```bash
docker run -p 80:80 \
  -e COMMANDS__HTTPBODY__QUERY=response \
  -e COMMANDS__HTTPCODE__QUERY=code \
  echoserver:latest
```

### Docker-Compose

```yaml
services:
  echoserver:
    image: echoserver:latest
    environment:
      - COMMANDS__HTTPBODY__QUERY=body
      - COMMANDS__HTTPCODE__QUERY=status
      - COMMANDS__TIME__QUERY=delay
```

### Kubernetes

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: echoserver-commands
data:
  COMMANDS__HTTPBODY__QUERY: "response_body"
  COMMANDS__HTTPCODE__QUERY: "response_code"
  COMMANDS__TIME__QUERY: "response_delay"
```

Update at runtime:

```bash
kubectl patch configmap echoserver-commands \
  -p '{"data":{"COMMANDS__HTTPBODY__QUERY":"new_body"}}'

kubectl rollout restart deployment/echoserver
```

---

**Related:** [Configuration →]({{ site.baseurl }}/configuration/)
