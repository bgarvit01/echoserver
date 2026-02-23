"""
Response handler strategies for different types of echo server responses.

This module implements the Strategy pattern to handle different types of responses
based on the request parameters and headers.
"""

import os
import json
import random
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List, Tuple
from urllib.parse import ParseResult

from .config import ServerConfig
from .utils.file_utils import FileManager
from .utils.network_utils import NetworkUtils


class ResponseStrategy(ABC):
    """Abstract base class for response strategies."""
    
    def __init__(self, config: ServerConfig):
        self.config = config
    
    @abstractmethod
    def can_handle(self, headers: Dict[str, str], query: Dict[str, List[str]]) -> bool:
        """Check if this strategy can handle the request."""
        pass
    
    @abstractmethod
    def generate_response(self, headers: Dict[str, str], query: Dict[str, List[str]], 
                         parsed_path: ParseResult, body: str, client_address: tuple) -> str:
        """Generate the response content."""
        pass


class CustomBodyStrategy(ResponseStrategy):
    """Handle custom body responses from headers or query parameters."""
    
    def can_handle(self, headers: Dict[str, str], query: Dict[str, List[str]]) -> bool:
        """Check if custom body is requested."""
        # Check headers case-insensitively
        headers_lower = {k.lower(): v for k, v in headers.items()}
        return (self.config.commands.http_body_header.lower() in headers_lower or 
                self.config.commands.http_body_query in query)
    
    def generate_response(self, headers: Dict[str, str], query: Dict[str, List[str]], 
                         parsed_path: ParseResult, body: str, client_address: tuple) -> str:
        """Return the custom body content."""
        # Check headers case-insensitively
        headers_lower = {k.lower(): v for k, v in headers.items()}
        if self.config.commands.http_body_header.lower() in headers_lower:
            return headers_lower[self.config.commands.http_body_header.lower()]
        elif self.config.commands.http_body_query in query:
            return query[self.config.commands.http_body_query][0]
        return ""


class EnvironmentBodyStrategy(ResponseStrategy):
    """Handle environment variable body responses."""
    
    def can_handle(self, headers: Dict[str, str], query: Dict[str, List[str]]) -> bool:
        """Check if environment variable body is requested."""
        headers_lower = {k.lower(): v for k, v in headers.items()}
        return (self.config.commands.http_env_body_header.lower() in headers_lower or 
                self.config.commands.http_env_body_query in query)
    
    def generate_response(self, headers: Dict[str, str], query: Dict[str, List[str]], 
                         parsed_path: ParseResult, body: str, client_address: tuple) -> str:
        """Return environment variable content."""
        env_var_name = None
        headers_lower = {k.lower(): v for k, v in headers.items()}
        
        if self.config.commands.http_env_body_header.lower() in headers_lower:
            env_var_name = headers_lower[self.config.commands.http_env_body_header.lower()]
        elif self.config.commands.http_env_body_query in query:
            env_var_name = query[self.config.commands.http_env_body_query][0]
        
        if env_var_name:
            return os.getenv(env_var_name, '')
        return ""


class FileOperationStrategy(ResponseStrategy):
    """Handle file and directory operations."""
    
    def __init__(self, config: ServerConfig):
        super().__init__(config)
        self.file_manager = FileManager()
    
    def can_handle(self, headers: Dict[str, str], query: Dict[str, List[str]]) -> bool:
        """Check if file operation is requested and enabled."""
        if not self.config.features.enable_file:
            return False
        headers_lower = {k.lower(): v for k, v in headers.items()}
        return (self.config.commands.file_header.lower() in headers_lower or 
                self.config.commands.file_query in query)
    
    def generate_response(self, headers: Dict[str, str], query: Dict[str, List[str]], 
                         parsed_path: ParseResult, body: str, client_address: tuple) -> str:
        """Return file content or directory listing."""
        file_path = None
        headers_lower = {k.lower(): v for k, v in headers.items()}
        
        if self.config.commands.file_header.lower() in headers_lower:
            file_path = headers_lower[self.config.commands.file_header.lower()]
        elif self.config.commands.file_query in query:
            file_path = query[self.config.commands.file_query][0]
        
        if file_path:
            return self.file_manager.read_file_or_directory(file_path)
        return json.dumps({"error": "No file path specified"})


class DefaultEchoStrategy(ResponseStrategy):
    """Default echo response with structured JSON data."""
    
    def __init__(self, config: ServerConfig):
        super().__init__(config)
        self.network_utils = NetworkUtils()
    
    def can_handle(self, headers: Dict[str, str], query: Dict[str, List[str]]) -> bool:
        """This strategy handles all requests as fallback."""
        return True
    
    def generate_response(self, headers: Dict[str, str], query: Dict[str, List[str]], 
                         parsed_path: ParseResult, body: str, client_address: tuple) -> str:
        """Generate comprehensive echo response."""
        response_data = {}
        
        # Server hosting port and instance ID
        response_data["server_hosting_port"] = self.config.port
        response_data["server_unique_id"] = self.config.instance_id
        
        # Host information
        if self.config.features.enable_host:
            response_data["host"] = self._build_host_info()
        
        # HTTP information
        if self.config.features.enable_http:
            response_data["http"] = self._build_http_info(headers, parsed_path)
        
        # Request information
        if self.config.features.enable_request:
            response_data["request"] = self._build_request_info(
                headers, query, body, client_address
            )
        
        # Environment information (if enabled)
        if self.config.features.enable_env:
            response_data["environment"] = dict(os.environ)
        
        return json.dumps(response_data, indent=2)
    
    def _build_host_info(self) -> Dict[str, Any]:
        """Build host information section."""
        return {
            "hostname": self.network_utils.get_hostname(),
            "ip": self.network_utils.get_primary_ip(),
            "ips": self.network_utils.get_all_ips(),
            "os": {
                "platform": os.name,
                "release": "unknown",
                "type": "unknown"
            }
        }
    
    def _build_http_info(self, headers: Dict[str, str], parsed_path: ParseResult) -> Dict[str, Any]:
        """Build HTTP information section."""
        host_header = headers.get('Host', 'localhost')
        return {
            "method": headers.get('REQUEST_METHOD', 'GET'),
            "baseUrl": f"http://{host_header}",
            "originalUrl": str(parsed_path.geturl()) if hasattr(parsed_path, 'geturl') else parsed_path.path,
            "protocol": "http"
        }
    
    def _build_request_info(self, headers: Dict[str, str], query: Dict[str, List[str]], 
                           body: str, client_address: tuple) -> Dict[str, Any]:
        """Build request information section."""
        request_info = {
            "params": {},
            "query": {k: v[0] if len(v) == 1 else v for k, v in query.items()},
            "body": body,
            "headers": headers,
            "remoteAddress": client_address[0],
            "remotePort": client_address[1]
        }
        
        # Add cookies if enabled
        if self.config.features.enable_cookies:
            request_info["cookies"] = self._parse_cookies(headers)
        
        return request_info
    
    def _parse_cookies(self, headers: Dict[str, str]) -> Dict[str, str]:
        """Parse cookies from request headers."""
        cookies = {}
        cookie_header = headers.get('Cookie', '')
        if cookie_header:
            for cookie in cookie_header.split(';'):
                if '=' in cookie:
                    key, value = cookie.strip().split('=', 1)
                    cookies[key] = value
        return cookies


class ResponseManager:
    """Manages response strategy selection and execution."""
    
    def __init__(self, config: ServerConfig):
        self.config = config
        self.strategies = [
            CustomBodyStrategy(config),
            EnvironmentBodyStrategy(config),
            FileOperationStrategy(config),
            DefaultEchoStrategy(config),  # Must be last as fallback
        ]
    
    def generate_response(self, headers: Dict[str, str], query: Dict[str, List[str]], 
                         parsed_path: ParseResult, body: str, client_address: tuple) -> str:
        """Generate response using the first applicable strategy."""
        for strategy in self.strategies:
            if strategy.can_handle(headers, query):
                return strategy.generate_response(headers, query, parsed_path, body, client_address)
        
        # Fallback (should never reach here due to DefaultEchoStrategy)
        return json.dumps({"error": "No suitable response strategy found"})


class StatusCodeManager:
    """Manages status code selection including random selection from multiple codes."""
    
    def __init__(self, config: ServerConfig):
        self.config = config
    
    def get_status_code(self, headers: Dict[str, str], query: Dict[str, List[str]]) -> int:
        """Get status code from headers or query parameters."""
        code_str = self._get_code_string(headers, query)
        return self._parse_status_code(code_str)
    
    def _get_code_string(self, headers: Dict[str, str], query: Dict[str, List[str]]) -> str:
        """Extract status code string from headers or query."""
        headers_lower = {k.lower(): v for k, v in headers.items()}
        if self.config.commands.http_code_header.lower() in headers_lower:
            return headers_lower[self.config.commands.http_code_header.lower()]
        elif self.config.commands.http_code_query in query:
            return query[self.config.commands.http_code_query][0]
        return "200"
    
    def _parse_status_code(self, code_str: str) -> int:
        """Parse status code, handling multiple codes with random selection."""
        if '-' in code_str:
            try:
                codes = [int(c.strip()) for c in code_str.split('-')]
                # Validate all codes are valid HTTP status codes
                valid_codes = [code for code in codes if 100 <= code <= 599]
                if valid_codes:
                    return random.choice(valid_codes)
            except ValueError:
                pass
        
        try:
            code = int(code_str)
            if 100 <= code <= 599:
                return code
        except ValueError:
            pass
        
        # Default to 200 if parsing fails
        return 200


class HeaderManager:
    """Manages custom header addition to responses."""
    
    def __init__(self, config: ServerConfig):
        self.config = config
    
    def should_add_custom_headers(self, headers: Dict[str, str], query: Dict[str, List[str]]) -> bool:
        """Check if custom headers should be added."""
        if not self.config.features.enable_header:
            return False
        headers_lower = {k.lower(): v for k, v in headers.items()}
        return (self.config.commands.http_headers_header.lower() in headers_lower or 
                self.config.commands.http_headers_query in query)
    
    def get_custom_headers(self, headers: Dict[str, str], query: Dict[str, List[str]]) -> List[Tuple[str, str]]:
        """Parse and return custom headers to add to response as list of tuples to support duplicates."""
        header_string = self._get_header_string(headers, query)
        if header_string:
            return self._parse_header_string(header_string)
        return []
    
    def _get_header_string(self, headers: Dict[str, str], query: Dict[str, List[str]]) -> str:
        """Extract header string from headers or query."""
        headers_lower = {k.lower(): v for k, v in headers.items()}
        if self.config.commands.http_headers_header.lower() in headers_lower:
            return headers_lower[self.config.commands.http_headers_header.lower()]
        elif self.config.commands.http_headers_query in query:
            return query[self.config.commands.http_headers_query][0]
        return ""
    
    def _parse_header_string(self, header_string: str) -> List[Tuple[str, str]]:
        """
        Parse header string format 'Key:Value, Key2:Value2' into list of tuples.
        
        Supports duplicate header names for cases like Set-Cookie.
        Special handling for comma-separated values:
        - For Set-Cookie headers, each cookie should be separate
        - For other headers, commas within values are preserved
        
        Examples:
        - "Set-Cookie:name1=value1, Set-Cookie:name2=value2" 
        - "Cache-Control:no-cache, max-age=0"
        - "Accept:text/html, application/xml"
        """
        custom_headers = []
        try:
            # First, try to handle the case where header names are explicitly repeated
            # e.g., "Set-Cookie:name1=value1, Set-Cookie:name2=value2"
            if self._has_repeated_header_names(header_string):
                custom_headers = self._parse_with_repeated_names(header_string)
            else:
                # Handle normal comma-separated header pairs
                # e.g., "Header1:value1, Header2:value2"
                custom_headers = self._parse_normal_headers(header_string)
                
        except Exception:
            # Return empty list if parsing fails
            pass
        
        return custom_headers
    
    def _has_repeated_header_names(self, header_string: str) -> bool:
        """Check if the header string contains repeated header names."""
        # Look for pattern like "HeaderName:value, HeaderName:value"
        header_names = []
        parts = header_string.split(',')
        for part in parts:
            if ':' in part:
                name = part.split(':', 1)[0].strip().lower()
                if name in header_names:
                    return True
                header_names.append(name)
        return False
    
    def _parse_with_repeated_names(self, header_string: str) -> List[Tuple[str, str]]:
        """Parse headers when header names are explicitly repeated."""
        headers = []
        # Split by comma and process each header individually
        parts = header_string.split(',')
        
        for part in parts:
            part = part.strip()
            if ':' in part:
                key, _, value = part.partition(':')
                key = key.strip()
                value = value.strip()
                if key and value:
                    headers.append((key, value))
        
        return headers
    
    def _parse_normal_headers(self, header_string: str) -> List[Tuple[str, str]]:
        """Parse normal header format where commas separate different headers."""
        headers = []
        
        # Handle special cases for headers that commonly have comma-separated values
        special_headers = {
            'set-cookie',  # Each cookie should be a separate header
            'www-authenticate',  # Multiple auth methods
            'warning',  # Multiple warnings
        }
        
        # Check if this looks like a Set-Cookie with multiple values
        if header_string.lower().startswith('set-cookie:'):
            # For Set-Cookie, we need to be more careful about comma splitting
            # since cookie values might contain commas
            return self._parse_set_cookie_headers(header_string)
        
        # For other headers, split by comma and treat as separate headers
        parts = header_string.split(',')
        
        for part in parts:
            part = part.strip()
            if ':' in part:
                key, _, value = part.partition(':')
                key = key.strip()
                value = value.strip()
                if key and value:
                    headers.append((key, value))
        
        return headers
    
    def _parse_set_cookie_headers(self, header_string: str) -> List[Tuple[str, str]]:
        """
        Special parsing for Set-Cookie headers.
        
        Set-Cookie values can contain commas, so we need to be more careful.
        Format: "Set-Cookie:name1=value1; Path=/; HttpOnly, name2=value2; Secure"
        """
        headers = []
        
        # Remove "Set-Cookie:" prefix if present
        if header_string.lower().startswith('set-cookie:'):
            cookie_values = header_string[11:].strip()
        else:
            cookie_values = header_string
        
        # Split cookies by looking for patterns like ", name=" or ", __name="
        # This is a simple heuristic - for production use, consider a proper cookie parser
        import re
        
        # Split on comma followed by word characters and equals (likely start of new cookie)
        cookie_parts = re.split(r',\s*(?=[a-zA-Z_][a-zA-Z0-9_]*=)', cookie_values)
        
        for cookie in cookie_parts:
            cookie = cookie.strip()
            if cookie:
                headers.append(('Set-Cookie', cookie))
        
        return headers
