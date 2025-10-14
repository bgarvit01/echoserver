---
layout: page
title: Quick-Start
nav_order: 2
permalink: /quick-start/
---

# Quick-Start

Get Echo Server running in minutes.

---

## Docker

Run Echo Server using Docker:

```bash
# Pull and run
docker run -p 80:80 echoserver:latest

# Or build from source
git clone https://github.com/bgarvit01/echoserver.git
cd echoserver
docker build -t echoserver:latest .
docker run -p 80:80 echoserver:latest
```

### With Configuration

```bash
docker run -p 80:80 \
  -e LOGS__LEVEL=info \
  -e ENABLE_FILE=false \
  -e ENABLE_ENV=false \
  echoserver:latest
```

[Full Docker Documentation →]({{ site.baseurl }}/docker/)

---

## Docker-Compose

Create a `docker-compose.yml`:

```yaml
version: "3.8"
services:
  echoserver:
    image: echoserver:latest
    ports:
      - "80:80"
    environment:
      - LOGS__LEVEL=info
      - ENABLE_FILE=false
```

Start the service:

```bash
docker-compose up -d
```

[Full Docker Compose Documentation →]({{ site.baseurl }}/docker-compose/)

---

## Kubernetes

Quick deployment:

```bash
# Deploy
kubectl apply -f https://raw.githubusercontent.com/bgarvit01/echoserver/main/k8s/echoserver-all.yaml

# Port forward for testing
kubectl port-forward -n echoserver service/echoserver 80:80

# Test
curl http://localhost:80
```

[Full Kubernetes Documentation →]({{ site.baseurl }}/kubernetes/)

---

## Testing Your Server

Once running, test with these commands:

```bash
# Basic echo
curl http://localhost:80

# Custom status code
curl -I http://localhost:80/?echo_code=404

# Custom body
curl http://localhost:80/?echo_body=hello

# Custom headers
curl -I http://localhost:80/?echo_header=Custom:Value

# Response delay (in milliseconds)
curl http://localhost:80/?echo_time=2000

# Multiple status codes (random)
curl -I http://localhost:80/?echo_code=200-400-500
```

---

## Response Format

```json
{
  "host": {
    "hostname": "echoserver-7d4c8c4f8b-xyz",
    "ip": "10.244.0.123",
    "ips": ["10.244.0.123"]
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
    "body": {}
  }
}
```

---

## Next Steps

- [Configuration]({{ site.baseurl }}/configuration/) - Customize server behavior
- [Feature-Toggle]({{ site.baseurl }}/feature-toggle/) - Enable/disable features
- [Commands]({{ site.baseurl }}/commands/) - Customize command parameters
