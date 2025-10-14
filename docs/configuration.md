---
layout: page
title: Configuration
nav_order: 6
permalink: /configuration/
---

# Configuration

Echo Server provides extensive configuration options through environment variables and command-line arguments.

---

## Server Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `127.0.0.1` | Server bind address |
| `PORT` | `80` | Server port |

### Example

```bash
export HOST=0.0.0.0
export PORT=8080
python run_server.py
```

---

## Logging Configuration

| Variable | Default | Options | Description |
|----------|---------|---------|-------------|
| `LOGS__LEVEL` | `debug` | `debug`, `info`, `warning`, `error` | Log level |
| `LOGS__FORMAT` | `default` | `default`, `line`, `object` | Log format |
| `LOGS__APP` | `echoserver` | any string | Application name in logs |

### Example

```bash
export LOGS__LEVEL=info
export LOGS__FORMAT=object
export LOGS__APP=myapp
```

---

## Feature Toggles

| Variable | Default | Description |
|----------|---------|-------------|
| `ENABLE_LOGS` | `true` | Enable logging |
| `ENABLE_HOST` | `true` | Include host information in response |
| `ENABLE_HTTP` | `true` | Include HTTP information in response |
| `ENABLE_REQUEST` | `true` | Include request details in response |
| `ENABLE_COOKIES` | `true` | Include cookies in response |
| `ENABLE_FILE` | `true` | Enable file operations |
| `ENABLE_HEADER` | `true` | Enable custom response headers |
| `ENABLE_ENV` | `false` | Include environment variables in response |

[Learn more about Feature-Toggle →]({{ site.baseurl }}/feature-toggle/)

---

## Control Limits

| Variable | Default | Description |
|----------|---------|-------------|
| `CONTROLS__TIMES__MIN` | `0` | Minimum delay in milliseconds |
| `CONTROLS__TIMES__MAX` | `60000` | Maximum delay in milliseconds |

### Example

```bash
export CONTROLS__TIMES__MIN=0
export CONTROLS__TIMES__MAX=5000
```

---

## Configuration Profiles

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

---

## Command Line Interface

View all available options:

```bash
python run_server.py --help
```

Override environment variables:

```bash
python run_server.py --host 0.0.0.0 --port 8080 --log-level info
```

---

## Related

- [Feature-Toggle]({{ site.baseurl }}/feature-toggle/) - Detailed feature control
- [Commands]({{ site.baseurl }}/commands/) - Customize command parameters
