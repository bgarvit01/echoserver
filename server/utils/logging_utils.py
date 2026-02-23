"""
Logging utilities for the Echo Server.
"""

import json
import logging
import datetime
from typing import Dict, List, Any
from urllib.parse import ParseResult

from ..config import ServerConfig, LogFormat


class RequestLogger:
    """Handles request logging with different formats."""
    
    def __init__(self, config: ServerConfig):
        """Initialize with configuration."""
        self.config = config
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logger with configuration."""
        logger = logging.getLogger(self.config.logging.app_name)
        logger.setLevel(self.config.logging.get_logging_level())
        
        # Clear any existing handlers
        logger.handlers.clear()
        
        # Create handler
        handler = logging.StreamHandler()
        
        # Set format based on configuration
        if self.config.logging.format == LogFormat.OBJECT:
            # For object format, we'll format in log_request method
            formatter = logging.Formatter('%(message)s')
        else:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Prevent propagation to avoid duplicate logs
        logger.propagate = False
        
        return logger
    
    def log_request(self, method: str, path: str, status_code: int, 
                   client_address: str, headers: Dict[str, str] = None,
                   query: Dict[str, List[str]] = None, body: str = "") -> None:
        """
        Log request based on configured format.
        
        Args:
            method: HTTP method
            path: Request path
            status_code: Response status code
            client_address: Client IP address
            headers: Request headers (optional)
            query: Query parameters (optional)
            body: Request body (optional)
        """
        if not self.config.features.enable_logs:
            return
        
        if self.config.logging.format == LogFormat.LINE:
            self._log_line_format(method, path, status_code)
        elif self.config.logging.format == LogFormat.OBJECT:
            self._log_object_format(method, path, status_code, client_address, 
                                  headers, query, body)
        else:  # DEFAULT format
            self._log_default_format(method, path, status_code, client_address)
    
    def _log_line_format(self, method: str, path: str, status_code: int) -> None:
        """Log in simple line format."""
        timestamp = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
        message = f"{timestamp} - {method} {path} - {status_code}"
        self.logger.info(message)
    
    def _log_object_format(self, method: str, path: str, status_code: int,
                          client_address: str, headers: Dict[str, str] = None,
                          query: Dict[str, List[str]] = None, body: str = "") -> None:
        """Log in structured JSON object format."""
        log_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "method": method,
            "path": path,
            "status": status_code,
            "client": client_address,
            "userAgent": (headers or {}).get('User-Agent', 'unknown'),
            "contentLength": len(body) if body else 0,
        }
        
        # Add query parameters if present
        if query:
            log_data["query"] = {k: v[0] if len(v) == 1 else v for k, v in query.items()}
        
        # Add selected headers (avoid logging sensitive information)
        if headers:
            safe_headers = {
                "host": headers.get('Host'),
                "contentType": headers.get('Content-Type'),
                "accept": headers.get('Accept'),
                "acceptEncoding": headers.get('Accept-Encoding'),
            }
            # Remove None values
            log_data["headers"] = {k: v for k, v in safe_headers.items() if v is not None}
        
        self.logger.info(json.dumps(log_data))
    
    def _log_default_format(self, method: str, path: str, status_code: int, 
                           client_address: str) -> None:
        """Log in default format."""
        message = f"{method} {path} - {status_code} - {client_address}"
        self.logger.info(message)
    
    def log_error(self, message: str, exception: Exception = None) -> None:
        """Log error messages."""
        if exception:
            self.logger.error(f"{message}: {str(exception)}")
        else:
            self.logger.error(message)
    
    def log_warning(self, message: str) -> None:
        """Log warning messages."""
        self.logger.warning(message)
    
    def log_info(self, message: str) -> None:
        """Log info messages."""
        self.logger.info(message)
    
    def get_logger(self) -> logging.Logger:
        """Get the underlying logger instance."""
        return self.logger
