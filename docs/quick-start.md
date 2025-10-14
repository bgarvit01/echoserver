---
layout: page
title: Quick Start
permalink: /quick-start/
---

# Quick Start

Get Echo Server running in minutes with your preferred deployment method.

## Prerequisites

Before you begin, ensure you have the required tools installed for your chosen deployment method:

### For Docker
- Docker Engine 20.10+
- Docker Compose 2.0+ (for Compose deployments)

### For Kubernetes
- Kubernetes cluster 1.19+
- kubectl configured for your cluster

## Basic Testing

Once your Echo Server is running, test it with these basic commands:

```bash
# Basic echo
curl http://your-echoserver/

# Custom status code
curl -I http://your-echoserver/?echo_code=404

# Custom body
curl http://your-echoserver/?echo_body=hello

# Custom headers
curl -I http://your-echoserver/?echo_header=Custom:Value
```

## Deployment Options

- [Docker Deployment](docker.html)
- [Docker Compose Setup](docker-compose.html)
- [Kubernetes Deployment](kubernetes.html)

## Next Steps

After completing the quick start:

1. Explore [Configuration](configuration.html) options
2. Learn about [Feature Toggles](feature-toggle.html)
3. Customize [Commands](commands.html)

