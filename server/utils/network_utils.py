"""
Network utility functions for the Echo Server.
"""

import socket
from typing import List
from functools import lru_cache


class NetworkUtils:
    """Utilities for network operations and information gathering."""
    
    def __init__(self):
        """Initialize NetworkUtils."""
        pass
    
    @lru_cache(maxsize=1)
    def get_hostname(self) -> str:
        """
        Get the server's hostname with caching.
        
        Returns:
            Hostname as string
        """
        try:
            return socket.gethostname()
        except Exception:
            return "unknown"
    
    @lru_cache(maxsize=1)
    def get_primary_ip(self) -> str:
        """
        Get the server's primary IP address with caching.
        
        Uses connection to a remote server to determine the local IP
        that would be used for outbound connections.
        
        Returns:
            Primary IP address as string
        """
        try:
            # Create a socket and connect to a remote address
            # This doesn't actually send data, just determines routing
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                # Use Google's DNS server as a remote endpoint
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"
    
    @lru_cache(maxsize=1)
    def get_all_ips(self) -> List[str]:
        """
        Get all IP addresses associated with the hostname with caching.
        
        Returns:
            List of IP addresses
        """
        try:
            hostname = self.get_hostname()
            # Get all addresses associated with hostname
            _, _, ip_list = socket.gethostbyname_ex(hostname)
            
            # Always include localhost
            ips = ["127.0.0.1"]
            
            # Add other IPs if they're not already included
            for ip in ip_list:
                if ip not in ips:
                    ips.append(ip)
            
            return ips
        except Exception:
            return ["127.0.0.1"]
    
    def clear_cache(self) -> None:
        """Clear the cached network information."""
        self.get_hostname.cache_clear()
        self.get_primary_ip.cache_clear()
        self.get_all_ips.cache_clear()
    
    @staticmethod
    def is_valid_port(port: int) -> bool:
        """
        Check if a port number is valid.
        
        Args:
            port: Port number to validate
            
        Returns:
            True if port is valid, False otherwise
        """
        return 1 <= port <= 65535
    
    @staticmethod
    def is_valid_host(host: str) -> bool:
        """
        Check if a hostname or IP address is valid.
        
        Args:
            host: Host to validate
            
        Returns:
            True if host appears valid, False otherwise
        """
        if not host or not host.strip():
            return False
        
        # Try to parse as IP address
        try:
            socket.inet_aton(host)
            return True
        except socket.error:
            pass
        
        # Check as hostname (basic validation)
        if len(host) > 253:
            return False
        
        # Allow alphanumeric, dots, and hyphens
        allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-')
        return all(c in allowed_chars for c in host)
    
    def get_network_info(self) -> dict:
        """
        Get comprehensive network information.
        
        Returns:
            Dictionary with network information
        """
        return {
            "hostname": self.get_hostname(),
            "primary_ip": self.get_primary_ip(),
            "all_ips": self.get_all_ips(),
            "family": "IPv4",  # Currently only support IPv4
        }
