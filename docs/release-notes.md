---
layout: page
title: Release Notes
permalink: /release-notes/
---

# Release Notes

## Version 2.0.0 (Latest)

### 🚀 New Features
- **Complete deployment support** - Docker, Docker Compose, and Kubernetes
- **Duplicate header support** - Multiple headers with same name (e.g., Set-Cookie)
- **Modular architecture** - Refactored for better maintainability
- **Enhanced security** - Non-root containers, security contexts, resource limits
- **Comprehensive configuration** - Environment variables, CLI args, ConfigMaps
- **Production-ready** - Health checks, autoscaling, ingress support

### 🔧 Improvements
- **Port 80 default** - Changed from 8000 to 80 for standard HTTP
- **5 replicas default** - Increased from 3 for better availability
- **Structured logging** - JSON format for log aggregation
- **Type hints** - Full Python type annotations
- **Documentation** - Complete Jekyll-based documentation site

### 🏗️ Architecture
- **Strategy Pattern** - Flexible response handling
- **Configuration Management** - Centralized config with dataclasses
- **Manager Classes** - Separated concerns (Status, Headers, Timing, etc.)
- **Utilities** - Network, file, timing, and logging utilities

### 📦 Deployment Options
- **Docker** - Multi-stage builds, security best practices
- **Docker Compose** - Development, production, and override configurations
- **Kubernetes** - Complete manifests with security contexts

### 🔐 Security Features
- **Non-root execution** - UID 1000 in containers
- **Dropped capabilities** - Minimal security context
- **Read-only filesystem** - Where possible
- **Resource limits** - Memory and CPU constraints
- **Path traversal protection** - Secure file operations

### 🧪 Testing
- **Comprehensive test suite** - 22 tests covering all features
- **CI/CD ready** - GitHub Actions for documentation
- **Validation tools** - kubectl dry-run support

## Version 1.0.0

### Initial Release
- Basic echo server functionality
- HTTP method support (GET, POST, PUT, PATCH, DELETE)
- Query parameter and header control
- Environment variable support
- File operations
- Custom status codes and bodies
- Response delays
- Basic Docker support

---

## Upgrading

### From 1.0.0 to 2.0.0

**⚠️ Breaking Changes:**
- Default port changed from 8000 to 80
- Configuration structure updated
- Docker image user changed to non-root

**Migration Steps:**

1. **Update port references:**
   ```bash
   # Old
   curl http://localhost:8000
   
   # New  
   curl http://localhost:80
   ```

2. **Update Docker commands:**
   ```bash
   # Old
   docker run -p 8000:8000 echoserver
   
   # New
   docker run -p 80:80 echoserver
   ```

3. **Update Kubernetes manifests:**
   ```yaml
   # Old
   containerPort: 8000
   
   # New
   containerPort: 80
   ```

4. **Environment variables** (optional):
   ```bash
   # New structured configuration available
   export LOGS__LEVEL=info
   export LOGS__FORMAT=object
   export ENABLE_FILE=false
   ```

## Compatibility

### Supported Versions
- **Docker**: 20.10+
- **Kubernetes**: 1.19+
- **Python**: 3.9+

### Supported Platforms
- **Linux**: x86_64, arm64
- **macOS**: Intel, Apple Silicon
- **Windows**: WSL2 recommended

## Support

- **GitHub Issues**: [Report bugs](https://github.com/bgarvit01/echoserver/issues)
- **Documentation**: [Full documentation](https://bgarvit01.github.io/echoserver/)
- **Discussions**: [Community discussions](https://github.com/bgarvit01/echoserver/discussions)

---

