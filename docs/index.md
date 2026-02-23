---
layout: home
title: Documentation
nav_order: 1
---

# Echo Server

HTTP request/response service for testing and debugging

[View on GitHub](https://github.com/bgarvit01/echoserver) | [Quick Start]({{ site.baseurl }}/quick-start/)

---

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## What is Echo Server?

An echo server replicates the request sent by the client and sends it back, making it perfect for:
- Testing and debugging HTTP requests
- Development and integration testing
- Learning about HTTP protocols
- Mock server for testing

## Features

- ✅ **All HTTP Methods** - GET, POST, PUT, PATCH, DELETE
- ✅ **Request Details** - Query parameters, body, IPs, host, URLs
- ✅ **Custom Headers** - Request headers and custom response headers (supports duplicates)
- ✅ **Environment Variables** - Access to server environment
- ✅ **Control via Headers/Query** - Custom responses, status codes, delays
- ✅ **File Operations** - Directory listing and file reading
- ✅ **Health Checks** - Built-in monitoring and structured logging
- ✅ **Production Ready** - Docker, Docker Compose, and Kubernetes support

## Quick Example

```bash
# Start the server
docker run -p 80:80 echoserver:latest

# Test it
curl http://localhost:80

# Custom response
curl http://localhost:80/?echo_code=404&echo_body=Not+Found
```

---

### [Get Started →]({{ site.baseurl }}/quick-start/)
