"""
Enhanced HTTP Echo Server with comprehensive features and clean architecture.

This module provides a refactored, maintainable HTTP echo server with:
- Configuration management via data classes
- Strategy pattern for response handling  
- Comprehensive logging and error handling
- Security controls for file operations
- Performance optimizations with caching
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from typing import Dict, List, Tuple, Optional, Any
import json
import asyncio
import threading

from .config import get_config, ServerConfig, set_config
from .response_handlers import ResponseManager, StatusCodeManager, HeaderManager
from .utils.timing_utils import TimingManager
from .utils.logging_utils import RequestLogger


class EchoRequestHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler with comprehensive echo server functionality.
    
    Features:
    - Multiple response strategies using Strategy pattern
    - Configurable timing controls with validation
    - Custom header support with multiple headers
    - File operations with security controls
    - Structured logging in multiple formats
    """
    
    def __init__(self, *args, **kwargs):
        """Initialize handler with configuration and managers."""
        self.config = get_config()
        self.response_manager = ResponseManager(self.config)
        self.status_manager = StatusCodeManager(self.config)
        self.header_manager = HeaderManager(self.config)
        self.timing_manager = TimingManager(self.config)
        self.request_logger = RequestLogger(self.config)
        super().__init__(*args, **kwargs)
    
    def _parse_request(self) -> Tuple[object, Dict[str, List[str]], str]:
        """
        Parse request components with error handling.
        
        Returns:
            Tuple of (parsed_path, query_params, body)
        """
        try:
            parsed_path = urlparse(self.path)
            query_params = parse_qs(parsed_path.query)
            body = self._get_request_body()
            return parsed_path, query_params, body
        except Exception as e:
            self.request_logger.log_error("Error parsing request", e)
            # Return safe defaults
            parsed_path = urlparse("/")
            return parsed_path, {}, ""
    
    def _get_request_body(self) -> str:
        """
        Safely read request body with size limits.
        
        Returns:
            Request body as string
        """
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            
            # Limit body size for security (10MB max)
            max_body_size = 10 * 1024 * 1024
            if content_length > max_body_size:
                self.request_logger.log_warning(
                    f"Request body too large: {content_length} bytes"
                )
                return ""
            
            if content_length > 0:
                body_bytes = self.rfile.read(content_length)
                return body_bytes.decode('utf-8', errors='replace')
            
            return ""
        except (ValueError, UnicodeDecodeError) as e:
            self.request_logger.log_error("Error reading request body", e)
            return ""
    
    def _handle_request(self) -> None:
        """
        Main request handling logic with comprehensive error handling.
        """
        try:
            # Parse request components
            parsed_path, query_params, body = self._parse_request()
            headers_dict = dict(self.headers)
            
            # Add method to headers for response handlers
            headers_dict['REQUEST_METHOD'] = self.command
            
            # Apply timing delay if requested
            self.timing_manager.apply_delay(headers_dict, query_params)
            
            # Determine response status code
            status_code = self.status_manager.get_status_code(headers_dict, query_params)
            
            # Generate response content
            response_content = self.response_manager.generate_response(
                headers_dict, query_params, parsed_path, body, self.client_address
            )
            
            # Send response
            self._send_response(status_code, headers_dict, query_params, response_content)
            
            # Log request
            self.request_logger.log_request(
                self.command, self.path, status_code, 
                self.client_address[0], headers_dict, query_params, body
            )
            
        except Exception as e:
            self.request_logger.log_error("Unexpected error handling request", e)
            self._send_error_response(500, "Internal Server Error")
    
    def _send_response(self, status_code: int, headers: Dict[str, str], 
                      query: Dict[str, List[str]], content: str) -> None:
        """
        Send HTTP response with proper headers.
        
        Args:
            status_code: HTTP status code
            headers: Request headers (for custom header extraction)
            query: Query parameters (for custom header extraction)
            content: Response content
        """
        try:
            # Send status
            self.send_response(status_code)
            
            # Add custom headers if requested
            custom_headers = self.header_manager.get_custom_headers(headers, query)
            headers_added = len(custom_headers) > 0
            
            for header_name, header_value in custom_headers:
                self.send_header(header_name, header_value)
            
            # Add default content type if no custom headers were added
            if not headers_added:
                self.send_header("Content-Type", "application/json")
            
            # Add server header
            self.send_header("Server", f"{self.config.logging.app_name}")
            
            # End headers
            self.end_headers()
            
            # Write response content
            self.wfile.write(content.encode('utf-8'))
            
        except Exception as e:
            self.request_logger.log_error("Error sending response", e)
    
    def _send_error_response(self, status_code: int, message: str) -> None:
        """
        Send error response with proper formatting.
        
        Args:
            status_code: HTTP error status code
            message: Error message
        """
        try:
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            
            error_response = {
                "error": {
                    "code": status_code,
                    "message": message
                }
            }
            
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
            
        except Exception:
            # If we can't even send an error response, just close the connection
            pass
    
    # HTTP method handlers - all delegate to _handle_request
    def do_GET(self) -> None:
        """Handle GET requests."""
        self._handle_request()
    
    def do_POST(self) -> None:
        """Handle POST requests."""
        self._handle_request()
    
    def do_PUT(self) -> None:
        """Handle PUT requests."""
        self._handle_request()
    
    def do_PATCH(self) -> None:
        """Handle PATCH requests."""
        self._handle_request()
    
    def do_DELETE(self) -> None:
        """Handle DELETE requests."""
        self._handle_request()
    
    def do_HEAD(self) -> None:
        """Handle HEAD requests."""
        self._handle_request()
    
    def do_OPTIONS(self) -> None:
        """Handle OPTIONS requests."""
        self._handle_request()
    
    def log_message(self, format_string: str, *args) -> None:
        """Suppress default HTTP server logging (we handle our own)."""
        # Suppress default logging to avoid duplication
        pass


class EchoServer:
    """
    Main Echo Server class with lifecycle management.
    
    Supports both HTTP/1.1 (via HTTPServer) and HTTP/2 (via hypercorn).
    """
    
    def __init__(self, config: Optional[ServerConfig] = None):
        """
        Initialize Echo Server.
        
        Args:
            config: Optional server configuration. If None, loads from environment.
        """
        if config:
            set_config(config)
        self.config = get_config()
        self.server: Optional[Any] = None  # Can be HTTPServer or hypercorn server
        self.logger = RequestLogger(self.config)
        self._server_thread: Optional[threading.Thread] = None
    
    def start(self) -> None:
        """
        Start the echo server.
        
        Uses HTTP/2 (hypercorn) if enable_http2 is True, otherwise uses HTTP/1.1 (HTTPServer).
        
        Raises:
            OSError: If unable to bind to the specified host/port
            Exception: For other server startup errors
        """
        try:
            protocol = "HTTP/2" if self.config.enable_http2 else "HTTP/1.1"
            self.logger.log_info(
                f"Starting Echo Server on http://{self.config.host}:{self.config.port} ({protocol})"
            )
            
            if self.config.enable_http2:
                self._start_http2()
            else:
                self._start_http11()
            
        except OSError as e:
            error_msg = f"Failed to start server on {self.config.host}:{self.config.port}"
            self.logger.log_error(error_msg, e)
            raise
        except KeyboardInterrupt:
            self.logger.log_info("Server shutdown requested")
            self.stop()
        except Exception as e:
            self.logger.log_error("Unexpected error starting server", e)
            raise
    
    def _start_http11(self) -> None:
        """Start HTTP/1.1 server using HTTPServer."""
        self.server = HTTPServer(
            (self.config.host, self.config.port), 
            EchoRequestHandler
        )
        
        self.logger.log_info("Echo Server is ready to accept connections (HTTP/1.1)")
        self.server.serve_forever()
    
    def _start_http2(self) -> None:
        """Start HTTP/2 server using hypercorn."""
        try:
            import hypercorn.asyncio
            from hypercorn.config import Config
            from .asgi_app import ASGIEchoApp
        except ImportError:
            raise ImportError(
                "HTTP/2 support requires hypercorn. Install it with: pip install hypercorn"
            )
        
        # Create ASGI application
        app = ASGIEchoApp()
        
        # Configure hypercorn
        config = Config()
        config.bind = [f"{self.config.host}:{self.config.port}"]
        config.use_reloader = False
        
        self.logger.log_info("Echo Server is ready to accept connections (HTTP/2)")
        
        # Run hypercorn
        asyncio.run(hypercorn.asyncio.serve(app, config))
    
    def stop(self) -> None:
        """Stop the echo server gracefully."""
        if self.server:
            self.logger.log_info("Stopping Echo Server...")
            if self.config.enable_http2:
                # Hypercorn handles shutdown via asyncio
                # The server will stop when the event loop is closed
                pass
            else:
                # HTTP/1.1 server shutdown
                self.server.shutdown()
                self.server.server_close()
            self.logger.log_info("Echo Server stopped")
    
    def get_server_info(self) -> Dict[str, any]:
        """
        Get server information.
        
        Returns:
            Dictionary with server information
        """
        return {
            "host": self.config.host,
            "port": self.config.port,
            "protocol": "HTTP/2" if self.config.enable_http2 else "HTTP/1.1",
            "app_name": self.config.logging.app_name,
            "features": {
                "logs": self.config.features.enable_logs,
                "host_info": self.config.features.enable_host,
                "http_info": self.config.features.enable_http,
                "request_info": self.config.features.enable_request,
                "cookies": self.config.features.enable_cookies,
                "file_operations": self.config.features.enable_file,
                "custom_headers": self.config.features.enable_header,
            },
            "timing": {
                "min_delay_ms": self.config.timing.min_delay_ms,
                "max_delay_ms": self.config.timing.max_delay_ms,
            },
            "commands": {
                "body_query": self.config.commands.http_body_query,
                "body_header": self.config.commands.http_body_header,
                "code_query": self.config.commands.http_code_query,
                "code_header": self.config.commands.http_code_header,
                "time_query": self.config.commands.time_query,
                "time_header": self.config.commands.time_header,
            }
        }


def start_server(host: str = "127.0.0.1", port: int = 80, 
                config: Optional[ServerConfig] = None) -> None:
    """
    Start the echo server with specified configuration.
    
    This function provides backward compatibility with the original interface.
    
    Args:
        host: Host to bind to
        port: Port to listen on
        config: Optional server configuration
    """
    if config is None:
        # Create config from parameters for backward compatibility
        from .config import ServerConfig
        config = get_config()
        config.host = host
        config.port = port
        set_config(config)
    
    server = EchoServer(config)
    server.start()


# For backward compatibility
def main() -> None:
    """Main entry point for backward compatibility."""
    start_server()


if __name__ == "__main__":
    main()
