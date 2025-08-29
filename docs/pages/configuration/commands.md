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

## Helm Configuration

### Values File
```yaml
# values.yaml
echoServer:
  commands:
    httpBodyQuery: "response_body"
    httpBodyHeader: "x-response-body"
    httpEnvBodyQuery: "env_response"
    httpEnvBodyHeader: "x-env-response"
    httpCodeQuery: "status_code"
    httpCodeHeader: "x-status-code"
    httpHeadersQuery: "custom_headers"
    httpHeadersHeader: "x-custom-headers"
    timeQuery: "delay_ms"
    timeHeader: "x-delay-ms"
    fileQuery: "file_path"
    fileHeader: "x-file-path"
```

### Template Usage
```yaml
# templates/configmap.yaml
data:
  COMMANDS__HTTPBODY__QUERY: {{ .Values.echoServer.commands.httpBodyQuery | quote }}
  COMMANDS__HTTPBODY__HEADER: {{ .Values.echoServer.commands.httpBodyHeader | quote }}
  COMMANDS__HTTPENVBODY__QUERY: {{ .Values.echoServer.commands.httpEnvBodyQuery | quote }}
  COMMANDS__HTTPENVBODY__HEADER: {{ .Values.echoServer.commands.httpEnvBodyHeader | quote }}
  COMMANDS__HTTPCODE__QUERY: {{ .Values.echoServer.commands.httpCodeQuery | quote }}
  COMMANDS__HTTPCODE__HEADER: {{ .Values.echoServer.commands.httpCodeHeader | quote }}
  COMMANDS__HTTPHEADERS__QUERY: {{ .Values.echoServer.commands.httpHeadersQuery | quote }}
  COMMANDS__HTTPHEADERS__HEADER: {{ .Values.echoServer.commands.httpHeadersHeader | quote }}
  COMMANDS__TIME__QUERY: {{ .Values.echoServer.commands.timeQuery | quote }}
  COMMANDS__TIME__HEADER: {{ .Values.echoServer.commands.timeHeader | quote }}
  COMMANDS__FILE__QUERY: {{ .Values.echoServer.commands.fileQuery | quote }}
  COMMANDS__FILE__HEADER: {{ .Values.echoServer.commands.fileHeader | quote }}
```

### Override Commands
```bash
helm install my-echo-server ./helm/echo-server \
  --set echoServer.commands.httpBodyQuery=custom_body \
  --set echoServer.commands.httpCodeQuery=status_code \
  --set echoServer.commands.timeQuery=delay_ms
```

## Use Case Examples

### API Testing Environment
Perfect for testing APIs with specific naming conventions:

```bash
export COMMANDS__HTTPBODY__QUERY=api_response
export COMMANDS__HTTPCODE__QUERY=api_status
export COMMANDS__HTTPHEADERS__QUERY=api_headers
export COMMANDS__TIME__QUERY=api_latency

# Usage
curl "http://localhost:80/?api_response=success&api_status=201&api_latency=100"
```

### Webhook Simulation
Configure for webhook testing:

```bash
export COMMANDS__HTTPBODY__QUERY=webhook_payload
export COMMANDS__HTTPCODE__QUERY=webhook_status
export COMMANDS__HTTPHEADERS__QUERY=webhook_headers

# Simulate webhook responses
curl "http://localhost:80/?webhook_payload=event_received&webhook_status=200"
```

### Legacy System Integration
Match existing system conventions:

```bash
export COMMANDS__HTTPBODY__QUERY=msg
export COMMANDS__HTTPCODE__QUERY=rc
export COMMANDS__TIME__QUERY=wait

# Usage matching legacy system
curl "http://localhost:80/?msg=operation_complete&rc=0&wait=500"
```

### Multi-language Support
Use localized command names:

```bash
# Spanish
export COMMANDS__HTTPBODY__QUERY=cuerpo
export COMMANDS__HTTPCODE__QUERY=codigo
export COMMANDS__TIME__QUERY=tiempo

# French  
export COMMANDS__HTTPBODY__QUERY=corps
export COMMANDS__HTTPCODE__QUERY=code
export COMMANDS__TIME__QUERY=temps

# German
export COMMANDS__HTTPBODY__QUERY=koerper
export COMMANDS__HTTPCODE__QUERY=code
export COMMANDS__TIME__QUERY=zeit
```

## Security Considerations

### Disable Sensitive Commands
For production environments, you can effectively disable commands by setting them to unlikely values:

```bash
# Make file operations harder to discover
export COMMANDS__FILE__QUERY=very_unlikely_file_command_name_12345
export COMMANDS__FILE__HEADER=x-very-unlikely-file-header-67890

# Make environment variable access harder
export COMMANDS__HTTPENVBODY__QUERY=extremely_obscure_env_command
export COMMANDS__HTTPENVBODY__HEADER=x-extremely-obscure-env-header
```

### Header Case Sensitivity
All header names are case-insensitive:

```bash
export COMMANDS__HTTPBODY__HEADER=x-custom-body

# All of these work
curl -H "X-Custom-Body: hello" http://localhost:80
curl -H "x-custom-body: hello" http://localhost:80
curl -H "X-CUSTOM-BODY: hello" http://localhost:80
```

## Validation and Testing

### Test Current Configuration
```bash
# Check what commands are currently configured
env | grep COMMANDS__

# Test custom body command
curl "http://localhost:80/?$(echo $COMMANDS__HTTPBODY__QUERY)=test"

# Test custom header command
curl -H "$(echo $COMMANDS__HTTPBODY__HEADER): test" http://localhost:80
```

### Validate Command Changes
```bash
# Test before deployment
python run_server.py &
SERVER_PID=$!

# Test custom commands
curl "http://localhost:80/?custom_body=test" | jq -r '.request.query'
curl -H "X-Custom-Body: test" http://localhost:80 | jq -r '.request.headers'

# Clean up
kill $SERVER_PID
```

## Troubleshooting

### Commands Not Working
```bash
# Check if commands are properly set
echo $COMMANDS__HTTPBODY__QUERY
echo $COMMANDS__HTTPBODY__HEADER

# Verify with environment listing
env | grep COMMANDS__

# Test with default commands
curl "http://localhost:80/?echo_body=test"
```

### Header Commands Not Working
```bash
# Check header name format
curl -v -H "$(echo $COMMANDS__HTTPBODY__HEADER): test" http://localhost:80

# Verify case insensitivity
curl -H "X-ECHO-BODY: test" http://localhost:80
curl -H "x-echo-body: test" http://localhost:80
```

### Kubernetes Command Updates
```bash
# Check ConfigMap
kubectl get configmap echo-server-commands -o yaml

# Verify pod environment
kubectl exec deployment/echo-server -- env | grep COMMANDS__

# Check if restart is needed
kubectl rollout status deployment/echo-server
```

## Best Practices

1. **Consistency**: Use consistent naming conventions across all commands
2. **Documentation**: Document custom command names for your team
3. **Security**: Use obscure names for sensitive commands in production
4. **Testing**: Always test command changes before deployment
5. **Backwards Compatibility**: Consider impact on existing integrations
6. **Case Sensitivity**: Remember headers are case-insensitive
7. **Environment Separation**: Use different command names per environment if needed
