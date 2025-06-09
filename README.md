# HTTP Echo Server

A full-featured HTTP Echo Server in Python.

## Features
- Supports GET, POST, PUT, PATCH, DELETE
- Echo request metadata (headers, query, body, IP)
- Control response using:
  - `echo_code`, `X-ECHO-CODE`
  - `echo_body`, `X-ECHO-BODY`
  - `echo_env_body`, `X-ECHO-ENV-BODY`
  - `echo_header`, `X-ECHO-HEADER`
  - `echo_time`, `X-ECHO-TIME`
  - `echo_file`, `X-ECHO-FILE`

## Run
```bash
python run_server.py --port 8000
```

## Test
```bash
pytest
```
