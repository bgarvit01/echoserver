import os
import time
import json
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

class EchoRequestHandler(BaseHTTPRequestHandler):
    def _parse_params(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        return parsed, query

    def _get_body(self):
        length = int(self.headers.get('Content-Length', 0))
        return self.rfile.read(length).decode() if length > 0 else ""

    def do_any(self):
        parsed_path, query = self._parse_params()
        body = self._get_body()

        # Delay if requested
        delay_ms = int(self.headers.get('X-ECHO-TIME', query.get('echo_time', [0])[0]))
        if delay_ms > 0:
            time.sleep(delay_ms / 1000.0)

        # Determine response code
        code = int(self.headers.get('X-ECHO-CODE', query.get('echo_code', [200])[0]))

        # Determine response body
        if 'X-ECHO-BODY' in self.headers:
            response = self.headers['X-ECHO-BODY']
        elif 'echo_body' in query:
            response = query['echo_body'][0]
        elif 'X-ECHO-ENV-BODY' in self.headers:
            response = os.getenv(self.headers['X-ECHO-ENV-BODY'], '')
        elif 'echo_env_body' in query:
            response = os.getenv(query['echo_env_body'][0], '')
        elif 'X-ECHO-FILE' in self.headers:
            response = self._read_file(self.headers['X-ECHO-FILE'])
        elif 'echo_file' in query:
            response = self._read_file(query['echo_file'][0])
        else:
            response = json.dumps({
                "method": self.command,
                "path": parsed_path.path,
                "query": query,
                "headers": dict(self.headers),
                "client_address": self.client_address[0],
                "body": body
            }, indent=2)

        # Optional echo headers
        if 'X-ECHO-HEADER' in self.headers:
            header_line = self.headers['X-ECHO-HEADER']
            key, _, value = header_line.partition(':')
            if key and value:
                self.send_response(code)
                self.send_header(key.strip(), value.strip())
        elif 'echo_header' in query:
            header_line = query['echo_header'][0]
            key, _, value = header_line.partition(':')
            if key and value:
                self.send_response(code)
                self.send_header(key.strip(), value.strip())
        else:
            self.send_response(code)
            self.send_header("Content-type", "application/json")

        self.end_headers()
        self.wfile.write(response.encode())

    def _read_file(self, path):
        try:
            if os.path.isdir(path):
                return json.dumps(os.listdir(path))
            elif os.path.isfile(path):
                with open(path, "r") as f:
                    return f.read()
            else:
                return "File or directory not found."
        except Exception as e:
            return str(e)

    def do_GET(self): self.do_any()
    def do_POST(self): self.do_any()
    def do_PUT(self): self.do_any()
    def do_PATCH(self): self.do_any()
    def do_DELETE(self): self.do_any()

    def log_message(self, format, *args):
        return  # Suppress standard logging

def start_server(host='127.0.0.1', port=8000):
    server = HTTPServer((host, port), EchoRequestHandler)
    print(f"HTTP Echo Server running on http://{host}:{port}")
    server.serve_forever()
