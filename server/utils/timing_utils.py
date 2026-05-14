"""
Timing utilities for request delays and validation.
"""

import time
from typing import Dict, List, Optional, Union

from ..config import ServerConfig


class TimingManager:
    """Manages request timing and delays with validation."""
    
    def __init__(self, config: ServerConfig):
        """Initialize with configuration."""
        self.config = config
    
    def get_delay_ms(self, headers: Dict[str, str], query: Dict[str, List[str]]) -> int:
        """
        Extract and validate delay from headers or query parameters.
        
        Args:
            headers: Request headers
            query: Query parameters
            
        Returns:
            Validated delay in milliseconds
        """
        delay_str = self._extract_delay_string(headers, query)
        return self._validate_delay(delay_str)
    
    def apply_delay(self, headers: Dict[str, str], query: Dict[str, List[str]]) -> None:
        """
        Apply delay if requested and within limits.
        
        Args:
            headers: Request headers
            query: Query parameters
        """
        delay_ms = self.get_delay_ms(headers, query)
        if delay_ms > 0:
            time.sleep(delay_ms / 1000.0)
    
    def _extract_delay_string(self, headers: Dict[str, str], query: Dict[str, List[str]]) -> str:
        """Extract delay string from headers or query parameters."""
        # Check headers first (higher priority) - case insensitive
        headers_lower = {k.lower(): v for k, v in headers.items()}
        if self.config.commands.time_header.lower() in headers_lower:
            return headers_lower[self.config.commands.time_header.lower()]
        
        # Check query parameters
        if self.config.commands.time_query in query:
            return query[self.config.commands.time_query][0]
        
        return "0"
    
    def _validate_delay(self, delay_str: str) -> int:
        """
        Validate and clamp delay within configured limits.
        
        Args:
            delay_str: String representation of delay
            
        Returns:
            Validated delay in milliseconds
        """
        try:
            delay_ms = int(delay_str)
        except (ValueError, TypeError):
            return 0
        
        # Apply configured limits
        if delay_ms < self.config.timing.min_delay_ms:
            return self.config.timing.min_delay_ms
        elif delay_ms > self.config.timing.max_delay_ms:
            return self.config.timing.max_delay_ms
        
        return delay_ms
    
    def get_silent_drop_ms(self, headers: Dict[str, str],
                           query: Dict[str, List[str]]) -> Optional[int]:
        """
        Determine if the caller asked the server to silently drop this request.

        A "silent drop" means: read the request fully, then sleep for the
        requested number of milliseconds and close the connection without
        ever sending a response. This is meant to simulate a backend that
        accepts the TCP connection and the request bytes but never replies,
        so that clients can be tested for correct idle-timeout / connection
        cleanup behavior (see ENG-809879).

        Accepted values (from header or query parameter):
            - "true" / "1" / "yes" / "on" / "" -> use ``timing.max_delay_ms``
            - any positive integer string       -> sleep that many ms
              (clamped to the configured min/max delay)

        Returns:
            Sleep duration in milliseconds, or ``None`` if silent-drop was
            not requested.
        """
        headers_lower = {k.lower(): v for k, v in headers.items()}

        raw_value: Optional[str] = None
        if self.config.commands.silent_drop_header.lower() in headers_lower:
            raw_value = headers_lower[
                self.config.commands.silent_drop_header.lower()
            ]
        elif self.config.commands.silent_drop_query in query:
            values = query[self.config.commands.silent_drop_query]
            raw_value = values[0] if values else ""
        else:
            return None

        normalized = (raw_value or "").strip().lower()

        # Treat enabling-only values (no explicit duration) as "use the
        # configured max delay" so the simplest invocation just works.
        if normalized in ("", "true", "1", "yes", "on"):
            return max(self.config.timing.max_delay_ms,
                       self.config.timing.min_delay_ms)

        # Any explicitly disabling value short-circuits to "no drop".
        if normalized in ("false", "0", "no", "off"):
            return None

        try:
            ms = int(normalized)
        except (ValueError, TypeError):
            return None

        if ms <= 0:
            return None

        return self._validate_delay(str(ms))

    def is_delay_within_limits(self, delay_ms: int) -> bool:
        """
        Check if delay is within configured limits.
        
        Args:
            delay_ms: Delay in milliseconds
            
        Returns:
            True if within limits, False otherwise
        """
        return (self.config.timing.min_delay_ms <= delay_ms <= 
                self.config.timing.max_delay_ms)
    
    def get_timing_info(self) -> Dict[str, Union[int, bool]]:
        """
        Get timing configuration information.
        
        Returns:
            Dictionary with timing configuration
        """
        return {
            "min_delay_ms": self.config.timing.min_delay_ms,
            "max_delay_ms": self.config.timing.max_delay_ms,
            "timing_enabled": True,
        }
