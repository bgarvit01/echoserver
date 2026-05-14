"""
ASGI application wrapper for HTTP/2 support.

This module provides an ASGI-compatible interface for the echo server,
enabling HTTP/2 support via hypercorn.
"""

from typing import Dict, List, Tuple, Optional, Any
import asyncio
import json
from urllib.parse import urlparse, parse_qs

from .config import get_config
from .response_handlers import ResponseManager, StatusCodeManager, HeaderManager
from .utils.timing_utils import TimingManager
from .utils.logging_utils import RequestLogger


class ASGIEchoApp:
    """
    ASGI application wrapper for the echo server.
    
    This allows the echo server to run with HTTP/2 support via hypercorn.
    """
    
    def __init__(self):
        """Initialize ASGI application with configuration."""
        self.config = get_config()
        self.response_manager = ResponseManager(self.config)
        self.status_manager = StatusCodeManager(self.config)
        self.header_manager = HeaderManager(self.config)
        self.timing_manager = TimingManager(self.config)
        self.request_logger = RequestLogger(self.config)
    
    async def __call__(self, scope: Dict[str, Any], receive, send) -> None:
        """
        ASGI application callable.
        
        Args:
            scope: ASGI scope dictionary
            receive: ASGI receive callable
            send: ASGI send callable
        """
        if scope["type"] != "http":
            # Only handle HTTP requests
            await send({
                "type": "http.response.start",
                "status": 400,
                "headers": [[b"content-type", b"application/json"]],
            })
            await send({
                "type": "http.response.body",
                "body": json.dumps({"error": "Only HTTP requests are supported"}).encode(),
            })
            return
        
        try:
            await self._handle_request(scope, receive, send)
        except Exception as e:
            self.request_logger.log_error("Unexpected error handling request", e)
            await self._send_error_response(500, "Internal Server Error", send)
    
    async def _handle_request(self, scope: Dict[str, Any], receive, send) -> None:
        """Handle HTTP request."""
        # Parse request components
        method = scope["method"]
        path = scope["path"]
        query_string = scope.get("query_string", b"").decode("utf-8")
        headers_dict = {name.decode().lower(): value.decode() for name, value in scope.get("headers", [])}
        
        # Parse query parameters
        parsed_path = urlparse(path)
        query_params = parse_qs(parsed_path.query)
        
        # Read request body
        body = await self._read_body(receive)
        
        # Get client address
        client_address = (scope.get("client", ["unknown"])[0], scope.get("client", [0, 0])[1])
        
        # Add method to headers for response handlers
        headers_dict['REQUEST_METHOD'] = method

        # Silent-drop short-circuit: read the request fully, sleep for the
        # requested duration, then close the connection without sending a
        # response. Used to simulate a backend that hangs (ENG-809879).
        silent_drop_ms = self.timing_manager.get_silent_drop_ms(
            headers_dict, query_params
        )
        if silent_drop_ms is not None:
            await self._silent_drop(
                method, path, client_address, silent_drop_ms, send
            )
            return

        # Apply timing delay if requested
        self.timing_manager.apply_delay(headers_dict, query_params)
        
        # Determine response status code
        status_code = self.status_manager.get_status_code(headers_dict, query_params)
        
        # Generate response content
        response_content = self.response_manager.generate_response(
            headers_dict, query_params, parsed_path, body, client_address
        )
        
        # Get custom headers
        custom_headers = self.header_manager.get_custom_headers(headers_dict, query_params)
        
        # Prepare response headers
        response_headers: List[Tuple[bytes, bytes]] = []
        
        # Add custom headers
        for header_name, header_value in custom_headers:
            response_headers.append((header_name.encode(), header_value.encode()))
        
        # Add default content type if no custom headers were added
        if not custom_headers:
            response_headers.append((b"content-type", b"application/json"))
        
        # Add server header
        response_headers.append((b"server", self.config.logging.app_name.encode()))
        
        # Send response
        await send({
            "type": "http.response.start",
            "status": status_code,
            "headers": response_headers,
        })
        
        await send({
            "type": "http.response.body",
            "body": response_content.encode("utf-8"),
        })
        
        # Log request
        self.request_logger.log_request(
            method, path, status_code,
            client_address[0], headers_dict, query_params, body
        )
    
    async def _read_body(self, receive) -> str:
        """Read request body from ASGI receive callable."""
        body_parts: List[bytes] = []
        
        while True:
            message = await receive()
            if message["type"] == "http.request":
                body_parts.append(message.get("body", b""))
                if not message.get("more_body", False):
                    break
            elif message["type"] == "http.disconnect":
                break
        
        body_bytes = b"".join(body_parts)
        
        # Limit body size for security (10MB max)
        max_body_size = 10 * 1024 * 1024
        if len(body_bytes) > max_body_size:
            self.request_logger.log_warning(
                f"Request body too large: {len(body_bytes)} bytes"
            )
            return ""
        
        try:
            return body_bytes.decode("utf-8", errors="replace")
        except UnicodeDecodeError as e:
            self.request_logger.log_error("Error decoding request body", e)
            return ""
    
    async def _silent_drop(self, method: str, path: str,
                           client_address: tuple, sleep_ms: int, send) -> None:
        """
        Simulate a silently-dropped request on the ASGI / HTTP/2 path.

        The request and headers are already consumed by the time we get
        here, so the client believes the request was accepted. We then
        sleep for ``sleep_ms`` milliseconds and ask the ASGI server to
        close the connection by sending an empty body with
        ``Connection: close`` and a 502 status. ASGI does not expose the
        raw socket the way the threaded HTTP/1.1 path does, so this is the
        closest approximation: the client will either time out (idle
        timeout) before we reply, or see a connection-close once the
        sleep elapses.

        Args:
            method: HTTP method (for logging).
            path: Request path (for logging).
            client_address: ``(host, port)`` of the remote peer.
            sleep_ms: How long to hold the connection open before closing.
            send: ASGI ``send`` callable.
        """
        client = f"{client_address[0]}:{client_address[1]}"
        self.request_logger.log_info(
            f"Silently dropping {method} {path} from {client}; "
            f"sleeping {sleep_ms}ms before closing connection"
        )

        try:
            await asyncio.sleep(sleep_ms / 1000.0)
        except asyncio.CancelledError:
            self.request_logger.log_info(
                f"Silent-drop sleep cancelled for {client}"
            )
            raise
        except Exception as e:
            self.request_logger.log_error(
                "Error during silent-drop sleep", e
            )

        self.request_logger.log_info(
            f"Closing silently-dropped connection from {client}"
        )

        try:
            await send({
                "type": "http.response.start",
                "status": 502,
                "headers": [(b"connection", b"close")],
            })
            await send({
                "type": "http.response.body",
                "body": b"",
                "more_body": False,
            })
        except Exception:
            # Client already gone; nothing to do.
            pass

    async def _send_error_response(self, status_code: int, message: str, send) -> None:
        """Send error response."""
        error_response = {
            "error": {
                "code": status_code,
                "message": message
            }
        }
        
        await send({
            "type": "http.response.start",
            "status": status_code,
            "headers": [[b"content-type", b"application/json"]],
        })
        
        await send({
            "type": "http.response.body",
            "body": json.dumps(error_response).encode("utf-8"),
        })

