---
layout: default
title: Quick Start
nav_order: 2
has_children: true
permalink: /quick-start/
---

# Quick Start

Get Echo Server running in minutes with your preferred deployment method.

Choose your deployment platform:

- [Docker](docker) - Single container deployment
- [Docker Compose](docker-compose) - Multi-environment setup
- [Kubernetes](kubernetes) - Production-ready orchestration


## Prerequisites

Before you begin, ensure you have the required tools installed for your chosen deployment method:

### For Docker
- Docker Engine 20.10+
- Docker Compose 2.0+ (for Compose deployments)

### For Kubernetes
- Kubernetes cluster 1.19+
- kubectl configured for your cluster


- Kubernetes cluster access

## Basic Testing

Once your Echo Server is running, test it with these basic commands:

```bash
# Basic echo
curl http://your-echo-server/

# Custom status code
curl -I http://your-echo-server/?echo_code=404

# Custom body
curl http://your-echo-server/?echo_body=hello

# Custom headers
curl -I http://your-echo-server/?echo_header=Custom:Value
```

## Next Steps

After completing the quick start:

1. Explore [Configuration](../configuration/) options
2. Learn about [Feature Toggles](../configuration/feature-toggle)
3. Set up [Logging](../configuration/loggers)
4. Customize [Commands](../configuration/commands)
