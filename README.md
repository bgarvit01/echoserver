# HTTP Echo Server

A full-featured HTTP Echo Server in Python with comprehensive testing capabilities and advanced configuration options.

📚 **[Complete Documentation](https://bgarvit01.github.io/echoserver/)** | 🐳 **[Docker Hub](https://hub.docker.com/r/garvitbhateja/echoserver)**

## Features

### Core Functionality
- Supports all HTTP methods: GET, POST, PUT, PATCH, DELETE
- Echo complete request metadata (headers, query, body, IP, cookies)
- JSON response with structured host, http, and request information
- Configurable logging with multiple formats
- Environment variable and CLI configuration support

### Custom Response Controls

All controls support both query parameters and HTTP headers:

| Feature | Query Parameter | HTTP Header | Description |
|---------|----------------|-------------|-------------|
| Status Code | `?echo_code=404` | `X-ECHO-CODE: 404` | Custom HTTP status code |
| Multiple Status | `?echo_code=200-400-500` | `X-ECHO-CODE: 200-400-500` | Random selection from multiple codes |
| Custom Body | `?echo_body=text` | `X-ECHO-BODY: text` | Custom response body |
| Environment Body | `?echo_env_body=HOSTNAME` | `X-ECHO-ENV-BODY: HOSTNAME` | Response from environment variable |
| Custom Headers | `?echo_header=Key:Value,Key2:Value2` | `X-ECHO-HEADER: Key:Value,Key2:Value2` | Add custom response headers (supports duplicates) |
| Response Delay | `?echo_time=5000` | `X-ECHO-TIME: 5000` | Delay response (milliseconds) |
| File Operations | `?echo_file=/path` | `X-ECHO-FILE: /path` | Read file or list directory |

### Configuration

#### Environment Variables

**Server Configuration:**
- `PORT`: Server port (default: 80)
- `HOST`: Server host (default: 127.0.0.1)

**Control Limits:**
- `CONTROLS__TIMES__MIN`: Minimum delay in ms (default: 0)
- `CONTROLS__TIMES__MAX`: Maximum delay in ms (default: 60000)

**Logging:**
- `LOGS__APP`: Application name (default: echoserver)
- `LOGS__LEVEL`: Log level - debug, info, warning, error (default: debug)
- `LOGS__FORMAT`: Log format - default, line, object (default: default)

**Custom Command Names:**
- `COMMANDS__HTTPBODY__QUERY`: Body query parameter name (default: echo_body)
- `COMMANDS__HTTPBODY__HEADER`: Body header name (default: x-echo-body)
- `COMMANDS__HTTPENVBODY__QUERY`: Env body query parameter (default: echo_env_body)
- `COMMANDS__HTTPENVBODY__HEADER`: Env body header name (default: x-echo-env-body)
- `COMMANDS__HTTPCODE__QUERY`: Status code query parameter (default: echo_code)
- `COMMANDS__HTTPCODE__HEADER`: Status code header name (default: x-echo-code)
- `COMMANDS__HTTPHEADERS__QUERY`: Custom headers query parameter (default: echo_header)
- `COMMANDS__HTTPHEADERS__HEADER`: Custom headers header name (default: x-echo-header)
- `COMMANDS__TIME__QUERY`: Delay query parameter (default: echo_time)
- `COMMANDS__TIME__HEADER`: Delay header name (default: x-echo-time)
- `COMMANDS__FILE__QUERY`: File operation query parameter (default: echo_file)
- `COMMANDS__FILE__HEADER`: File operation header name (default: x-echo-file)

**Feature Toggles:**
- `ENABLE_LOGS`: Enable request logging (default: true)
- `ENABLE_HOST`: Include host info in response (default: true)
- `ENABLE_HTTP`: Include HTTP info in response (default: true)
- `ENABLE_REQUEST`: Include request info in response (default: true)
- `ENABLE_COOKIES`: Enable cookie parsing (default: true)
- `ENABLE_FILE`: Enable file operations (default: true)
- `ENABLE_HEADER`: Enable custom headers (default: true)

## Usage Examples

### Basic Echo
```bash
curl http://localhost:80
```

### Custom Status Code
```bash
curl -I http://localhost:80/?echo_code=404
curl -I -H "X-ECHO-CODE: 404" http://localhost:80
```

### Multiple Random Status Codes
```bash
# Will randomly return 200, 400, or 500
curl -I http://localhost:80/?echo_code=200-400-500
```

### Custom Response Body
```bash
curl http://localhost:80/?echo_body=hello
curl -H "X-ECHO-BODY: world" http://localhost:80
```

### Environment Variable Response
```bash
curl http://localhost:80/?echo_env_body=HOSTNAME
curl -H "X-ECHO-ENV-BODY: USER" http://localhost:80
```

### Custom Headers
```bash
# Single header
curl -I http://localhost:80/?echo_header=Custom:Value

# Multiple different headers
curl -I -H "X-ECHO-HEADER: Header1:Value1,Header2:Value2" http://localhost:80

# Duplicate headers (like Set-Cookie)
curl -I -H "X-ECHO-HEADER: Set-Cookie:sessionid=abc123, Set-Cookie:userid=456" http://localhost:80

# Mixed headers with duplicates
curl -I -H "X-ECHO-HEADER: Cache-Control:no-cache, Set-Cookie:session=123, Set-Cookie:user=456" http://localhost:80
```

### Response Delay
```bash
curl http://localhost:80/?echo_time=5000  # 5 second delay
curl -H "X-ECHO-TIME: 3000" http://localhost:80  # 3 second delay
```

### File Operations
```bash
curl http://localhost:80/?echo_file=/tmp  # List directory
curl http://localhost:80/?echo_file=/etc/hostname  # Read file
curl -H "X-ECHO-FILE: /usr" http://localhost:80
```

### Combined Features
```bash
curl -H "X-ECHO-CODE: 201" -H "X-ECHO-BODY: Success" -H "X-ECHO-HEADER: Location:/new-resource" http://localhost:80
```

## Installation & Running

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Basic Usage
```bash
python run_server.py
```

### Advanced Configuration
```bash
# With custom port and host
python run_server.py --port 8080 --host 0.0.0.0

# With custom timing limits
python run_server.py --controls:times:min 100 --controls:times:max 30000

# With custom logging
python run_server.py --logs:level info --logs:format object

# Disable certain features
python run_server.py --disable-file --disable-logs

# Custom command names
python run_server.py --commands:httpBody:query custom_body --commands:httpCode:header x-custom-code
```

### Environment Variable Configuration
```bash
export PORT=8080
export LOGS__LEVEL=info
export CONTROLS__TIMES__MAX=10000
export ENABLE_FILE=false
python run_server.py
```

## Testing

### Run All Tests
```bash
pytest
```

### Run Specific Test Categories
```bash
pytest tests/test_echo_server.py::TestBasicFunctionality
pytest tests/test_echo_server.py::TestCustomStatusCodes
pytest tests/test_echo_server.py::TestFileOperations
```

### Run with Coverage
```bash
pytest --cov=server --cov-report=html
```

## Response Structure

Default JSON response includes:

```json
{
  "host": {
    "hostname": "server-name",
    "ip": "192.168.1.100",
    "ips": ["127.0.0.1", "192.168.1.100"],
    "os": {
      "platform": "posix",
      "release": "unknown",
      "type": "unknown"
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
    "query": {"key": "value"},
    "cookies": {"session": "abc123"},
    "body": "",
    "headers": {...},
    "remoteAddress": "127.0.0.1",
    "remotePort": 54321
  },
  "environment": {...}
}
```

## Deployment Options

### Docker

#### Build and Run
```bash
# Build the image
docker build -t echoserver .

# Run with default settings
docker run -p 80:80 echoserver

# Run with custom configuration
docker run -p 8080:80 \
  -e LOGS__LEVEL=info \
  -e LOGS__FORMAT=object \
  -e ENABLE_FILE=false \
  echoserver
```

#### Pre-built Images
```bash
# Pull and run (replace with your registry)
docker pull your-registry/echoserver:latest
docker run -p 80:80 your-registry/echoserver:latest
```

### Docker Compose

#### Development
```bash
# Start development environment
cd docker-compose
docker-compose -f docker-compose.dev.yml up

# With file mounting for development
docker-compose -f docker-compose.dev.yml up --build
```

#### Production
```bash
# Start production environment
cd docker-compose
docker-compose -f docker-compose.prod.yml up -d

# Scale to multiple replicas
docker-compose -f docker-compose.prod.yml up -d --scale echoserver=5
```

### Kubernetes

#### Quick Deploy
```bash
# Deploy everything at once
curl -sL https://raw.githubusercontent.com/yourrepo/echoserver/main/k8s/echoserver-all.yaml | kubectl apply -f -

# Or download and customize
wget https://raw.githubusercontent.com/yourrepo/echoserver/main/k8s/echoserver-all.yaml
kubectl apply -f echoserver-all.yaml
```

#### Step by Step
```bash
# Deploy individual components
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

#### Access the Service
```bash
# Port forward for testing
kubectl port-forward -n echoserver service/echoserver 80:80

# Or via ingress (add to /etc/hosts: <ingress-ip> echo.local)
curl http://echo.local
```

### Helm

#### Install from Repository
```bash
# Add helm repository (replace with your helm repo)
helm repo add echoserver https://your-charts-repo/
helm repo update

# Install with default values
helm install my-echoserver echoserver/echoserver

# Install with custom values
helm install my-echoserver echoserver/echoserver \
  --set replicaCount=5 \
  --set echoServer.logs.level=info \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host=echo.mydomain.com
```

#### Install from Local Charts
```bash
# Install from local helm chart
helm install my-echoserver ./helm/echoserver

# Install with custom values file
helm install my-echoserver ./helm/echoserver -f my-values.yaml

# Upgrade existing installation
helm upgrade my-echoserver ./helm/echoserver
```

#### Helm Configuration Examples
```yaml
# my-values.yaml
replicaCount: 3

ingress:
  enabled: true
  hosts:
    - host: echo.mydomain.com
      paths:
        - path: /
          pathType: Prefix

echoServer:
  logs:
    level: "info"
    format: "object"
  features:
    enableFile: false
    enableEnv: false
  controls:
    timesMax: 10000
```

## Security Features

- Path traversal protection for file operations
- Configurable timing limits to prevent abuse
- Optional feature disabling for security
- Safe environment variable access
- Structured error responses

## Documentation

For comprehensive documentation including deployment guides, configuration options, and examples, visit:

🌐 **[https://bgarvit01.github.io/echoserver/](https://bgarvit01.github.io/echoserver/)**

The documentation includes:
- [Quick Start Guides](https://bgarvit01.github.io/echoserver/quick-start/) - Docker, Kubernetes
- [Configuration](https://bgarvit01.github.io/echoserver/configuration/) - Feature toggles, logging, commands
- [Release Notes](https://bgarvit01.github.io/echoserver/pages/release-notes) - Version history and migration guides

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Documentation Contributions
The documentation is built with Jekyll and hosted on GitHub Pages. To contribute:

1. Edit files in the `docs/` directory
2. Test locally: `cd docs && bundle exec jekyll serve`
3. Submit a pull request

Documentation is automatically deployed when changes are merged to `main`.

## License

MIT License
