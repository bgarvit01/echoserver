---
layout: default
title: Home
nav_order: 1
description: "Echo Server - HTTP request/response service for testing and debugging"
permalink: /
---

# Echo Server
{: .fs-9 }

HTTP request/response service for testing and debugging
{: .fs-6 .fw-300 }

[Get started now](#quick-start){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View it on GitHub](https://github.com/bgarvit01/echoserver){: .btn .fs-5 .mb-4 .mb-md-0 }

---

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)
![Helm](https://img.shields.io/badge/Helm-0F1689?style=for-the-badge&logo=Helm&labelColor=0F1689)

An echo server is a server that replicates the request sent by the client and sends it back.

## Features

Available:
- **GET / POST / PUT / PATCH / DELETE** - All HTTP methods supported
- **Request Details** - Query parameters, body, IPs, host, URLs
- **Headers** - Request headers and custom response headers (supports duplicates)
- **Environment Variables** - Access to server environment
- **Control via Headers/Query** - Custom responses, status codes, delays
- **File Operations** - Directory listing and file reading
- **Monitoring** - Health checks and structured logging

## Quick Start

### Docker
```bash
# Run with Docker
docker run -p 80:80 echo-server:latest

# Test the server
curl http://localhost:80
```

### Kubernetes
```bash
# Quick deployment
kubectl apply -f https://raw.githubusercontent.com/bgarvit01/echoserver/main/k8s/echo-server-all.yaml

# Port forward for testing
kubectl port-forward -n echo-server service/echo-server-service 80:80
```

### Helm
```bash
# Install with Helm
helm install my-echo-server ./helm/echo-server

# Install with custom values
helm install my-echo-server ./helm/echo-server -f examples/production-values.yaml
```

## Example Usage

### Basic Echo
```bash
curl http://localhost:80
```

### Custom Status Code
```bash
curl -I http://localhost:80/?echo_code=404
```

### Custom Body
```bash
curl http://localhost:80/?echo_body=hello
```

### Custom Headers
```bash
curl -I http://localhost:80/?echo_header=Custom:Value
```

### Multiple Status Codes (Random)
```bash
curl -I http://localhost:80/?echo_code=200-400-500
```

### Response Delay
```bash
curl http://localhost:80/?echo_time=2000
```

## Response Format

```json
{
  "host": {
    "hostname": "echo-server-7d4c8c4f8b-xyz",
    "ip": "10.244.0.123",
    "ips": ["10.244.0.123"],
    "os": {
      "hostname": "echo-server-7d4c8c4f8b-xyz",
      "type": "Linux",
      "platform": "linux",
      "architecture": "x64",
      "release": "5.4.0"
    }
  },
  "http": {
    "method": "GET",
    "baseUrl": "http://localhost:80",
    "originalUrl": "/path?query=value",
    "protocol": "http"
  },
  "request": {
    "params": {},
    "query": {"query": "value"},
    "headers": {
      "host": "localhost:80",
      "user-agent": "curl/7.68.0"
    },
    "body": {},
    "files": {}
  },
  "environment": {...}
}
```

## About the Project

Echo Server is a comprehensive HTTP testing tool built in Python, providing enterprise-grade deployment options including Docker, Kubernetes, and Helm support.

### Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

### License

Echo Server is distributed under the MIT License. See `LICENSE` for more information.

---

Copyright © 2024 Echo Server Team.
