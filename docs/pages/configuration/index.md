---
layout: default
title: Configuration
nav_order: 3
has_children: true
permalink: /configuration/
---

# Configuration

Echo Server provides extensive configuration options to customize behavior, logging, and features.

## Configuration Methods

Echo Server can be configured through:

1. **Environment Variables** - Primary configuration method
2. **Command Line Arguments** - Override environment variables
3. **Configuration Files** - For Kubernetes ConfigMaps and Docker Compose

## Quick Reference

### Server Configuration
- `HOST` - Server bind address (default: `127.0.0.1`)
- `PORT` - Server port (default: `80`)

### Logging Configuration
- `LOGS__LEVEL` - Log level: `debug`, `info`, `warning`, `error` (default: `debug`)
- `LOGS__FORMAT` - Log format: `default`, `line`, `object` (default: `default`)
- `LOGS__APP` - Application name in logs (default: `echo-server`)

### Feature Toggles
- `ENABLE_LOGS` - Enable logging (default: `true`)
- `ENABLE_HOST` - Include host information (default: `true`)
- `ENABLE_HTTP` - Include HTTP information (default: `true`)
- `ENABLE_REQUEST` - Include request details (default: `true`)
- `ENABLE_COOKIES` - Include cookies (default: `true`)
- `ENABLE_FILE` - Enable file operations (default: `true`)
- `ENABLE_HEADER` - Enable custom headers (default: `true`)
- `ENABLE_ENV` - Include environment variables (default: `false`)

### Control Limits
- `CONTROLS__TIMES__MIN` - Minimum delay in ms (default: `0`)
- `CONTROLS__TIMES__MAX` - Maximum delay in ms (default: `60000`)

## Configuration Examples

### Development
```bash
export LOGS__LEVEL=debug
export LOGS__FORMAT=default
export ENABLE_FILE=true
export ENABLE_ENV=true
```

### Production
```bash
export LOGS__LEVEL=info
export LOGS__FORMAT=object
export ENABLE_FILE=false
export ENABLE_ENV=false
export CONTROLS__TIMES__MAX=10000
```

### Security-focused
```bash
export ENABLE_FILE=false
export ENABLE_ENV=false
export ENABLE_COOKIES=false
export CONTROLS__TIMES__MAX=5000
```

## Command Line Interface

View all available options:
```bash
python run_server.py --help
```

Override environment variables:
```bash
python run_server.py --host 0.0.0.0 --port 8080 --log-level info
```

## Next Steps

- Learn about [Feature Toggles](feature-toggle) to control functionality
- Configure [Logging](loggers) for different environments  
- Customize [Commands](commands) for your specific needs
