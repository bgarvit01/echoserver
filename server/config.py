"""
Configuration management for the Echo Server.

This module provides centralized configuration management with validation,
type safety, and environment variable support.
"""

import os
import logging
import uuid
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from enum import Enum


class LogFormat(Enum):
    """Supported logging formats."""
    DEFAULT = "default"
    LINE = "line"
    OBJECT = "object"


class LogLevel(Enum):
    """Supported logging levels."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class CommandConfig:
    """Configuration for custom command names."""
    http_body_query: str = "echo_body"
    http_body_header: str = "x-echo-body"
    http_env_body_query: str = "echo_env_body"
    http_env_body_header: str = "x-echo-env-body"
    http_code_query: str = "echo_code"
    http_code_header: str = "x-echo-code"
    http_headers_query: str = "echo_header"
    http_headers_header: str = "x-echo-header"
    time_query: str = "echo_time"
    time_header: str = "x-echo-time"
    file_query: str = "echo_file"
    file_header: str = "x-echo-file"


@dataclass
class TimingControls:
    """Configuration for timing controls and validation."""
    min_delay_ms: int = 0
    max_delay_ms: int = 60000
    
    def __post_init__(self):
        """Validate timing configuration."""
        if self.min_delay_ms < 0:
            raise ValueError("Minimum delay must be non-negative")
        if self.max_delay_ms < self.min_delay_ms:
            raise ValueError("Maximum delay must be >= minimum delay")
        if self.max_delay_ms > 300000:  # 5 minutes max
            raise ValueError("Maximum delay cannot exceed 5 minutes (300000ms)")


@dataclass
class FeatureFlags:
    """Feature toggle configuration."""
    enable_logs: bool = True
    enable_host: bool = True
    enable_http: bool = True
    enable_request: bool = True
    enable_cookies: bool = True
    enable_file: bool = True
    enable_header: bool = True
    enable_env: bool = False  # Environment variables in response (security sensitive)


@dataclass
class LoggingConfig:
    """Logging configuration."""
    app_name: str = "echoserver"
    level: LogLevel = LogLevel.DEBUG
    format: LogFormat = LogFormat.DEFAULT
    
    def get_logging_level(self) -> int:
        """Convert LogLevel enum to logging module constant."""
        level_mapping = {
            LogLevel.DEBUG: logging.DEBUG,
            LogLevel.INFO: logging.INFO,
            LogLevel.WARNING: logging.WARNING,
            LogLevel.ERROR: logging.ERROR,
        }
        return level_mapping[self.level]


def _generate_instance_id() -> str:
    """Generate a unique instance ID for the server."""
    return str(uuid.uuid4())


@dataclass
class ServerConfig:
    """Main server configuration."""
    host: str = "127.0.0.1"
    port: int = 80
    enable_http2: bool = False
    instance_id: str = field(default_factory=_generate_instance_id)  # Unique UUID for this server instance
    commands: CommandConfig = field(default_factory=CommandConfig)
    timing: TimingControls = field(default_factory=TimingControls)
    features: FeatureFlags = field(default_factory=FeatureFlags)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    
    def __post_init__(self):
        """Validate server configuration."""
        if not (1 <= self.port <= 65535):
            raise ValueError(f"Port must be between 1 and 65535, got {self.port}")
        if not self.host.strip():
            raise ValueError("Host cannot be empty")


class ConfigurationManager:
    """Manages configuration loading from environment variables and CLI args."""
    
    ENV_PREFIX = "ECHO_SERVER_"
    
    @classmethod
    def from_environment(cls) -> ServerConfig:
        """Load configuration from environment variables."""
        def get_env_bool(key: str, default: bool) -> bool:
            """Get boolean value from environment variable."""
            value = os.getenv(key, str(default)).lower()
            return value in ('true', '1', 'yes', 'on')
        
        def get_env_int(key: str, default: int) -> int:
            """Get integer value from environment variable."""
            try:
                return int(os.getenv(key, str(default)))
            except ValueError:
                return default
        
        def get_env_enum(key: str, enum_class, default):
            """Get enum value from environment variable."""
            value = os.getenv(key, default.value).lower()
            for enum_val in enum_class:
                if enum_val.value == value:
                    return enum_val
            return default
        
        # Server configuration
        host = os.getenv('HOST', '127.0.0.1')
        port = get_env_int('PORT', 80)
        enable_http2 = get_env_bool('ENABLE_HTTP2', False)
        
        # Command configuration
        commands = CommandConfig(
            http_body_query=os.getenv('COMMANDS__HTTPBODY__QUERY', 'echo_body'),
            http_body_header=os.getenv('COMMANDS__HTTPBODY__HEADER', 'x-echo-body'),
            http_env_body_query=os.getenv('COMMANDS__HTTPENVBODY__QUERY', 'echo_env_body'),
            http_env_body_header=os.getenv('COMMANDS__HTTPENVBODY__HEADER', 'x-echo-env-body'),
            http_code_query=os.getenv('COMMANDS__HTTPCODE__QUERY', 'echo_code'),
            http_code_header=os.getenv('COMMANDS__HTTPCODE__HEADER', 'x-echo-code'),
            http_headers_query=os.getenv('COMMANDS__HTTPHEADERS__QUERY', 'echo_header'),
            http_headers_header=os.getenv('COMMANDS__HTTPHEADERS__HEADER', 'x-echo-header'),
            time_query=os.getenv('COMMANDS__TIME__QUERY', 'echo_time'),
            time_header=os.getenv('COMMANDS__TIME__HEADER', 'x-echo-time'),
            file_query=os.getenv('COMMANDS__FILE__QUERY', 'echo_file'),
            file_header=os.getenv('COMMANDS__FILE__HEADER', 'x-echo-file'),
        )
        
        # Timing controls
        timing = TimingControls(
            min_delay_ms=get_env_int('CONTROLS__TIMES__MIN', 0),
            max_delay_ms=get_env_int('CONTROLS__TIMES__MAX', 60000),
        )
        
        # Feature flags
        features = FeatureFlags(
            enable_logs=get_env_bool('ENABLE_LOGS', True),
            enable_host=get_env_bool('ENABLE_HOST', True),
            enable_http=get_env_bool('ENABLE_HTTP', True),
            enable_request=get_env_bool('ENABLE_REQUEST', True),
            enable_cookies=get_env_bool('ENABLE_COOKIES', True),
            enable_file=get_env_bool('ENABLE_FILE', True),
            enable_header=get_env_bool('ENABLE_HEADER', True),
            enable_env=get_env_bool('ENABLE_ENV', False),
        )
        
        # Logging configuration
        logging_config = LoggingConfig(
            app_name=os.getenv('LOGS__APP', 'echoserver'),
            level=get_env_enum('LOGS__LEVEL', LogLevel, LogLevel.DEBUG),
            format=get_env_enum('LOGS__FORMAT', LogFormat, LogFormat.DEFAULT),
        )
        
        return ServerConfig(
            host=host,
            port=port,
            enable_http2=enable_http2,
            commands=commands,
            timing=timing,
            features=features,
            logging=logging_config,
        )
    
    @classmethod
    def update_from_args(cls, config: ServerConfig, args) -> ServerConfig:
        """Update configuration with command line arguments."""
        if hasattr(args, 'host') and args.host:
            config.host = args.host
        if hasattr(args, 'port') and args.port:
            config.port = args.port
            
        # Update timing controls
        timing_args = getattr(args, 'controls_times_min', None)
        if timing_args is not None:
            config.timing.min_delay_ms = timing_args
        timing_args = getattr(args, 'controls_times_max', None)
        if timing_args is not None:
            config.timing.max_delay_ms = timing_args
            
        # Update logging
        if hasattr(args, 'logs_level') and args.logs_level:
            config.logging.level = LogLevel(args.logs_level)
        if hasattr(args, 'logs_format') and args.logs_format:
            config.logging.format = LogFormat(args.logs_format)
        if hasattr(args, 'logs_app') and args.logs_app:
            config.logging.app_name = args.logs_app
            
        # Update feature flags
        feature_mappings = {
            'disable_logs': ('enable_logs', False),
            'disable_host': ('enable_host', False),
            'disable_http': ('enable_http', False),
            'disable_request': ('enable_request', False),
            'disable_cookies': ('enable_cookies', False),
            'disable_file': ('enable_file', False),
            'disable_header': ('enable_header', False),
        }
        
        for arg_name, (feature_name, value) in feature_mappings.items():
            if hasattr(args, arg_name) and getattr(args, arg_name):
                setattr(config.features, feature_name, value)
                
        return config


# Global configuration instance
_config: Optional[ServerConfig] = None


def get_config() -> ServerConfig:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = ConfigurationManager.from_environment()
    return _config


def set_config(config: ServerConfig) -> None:
    """Set the global configuration instance."""
    global _config
    _config = config


def reload_config() -> ServerConfig:
    """Reload configuration from environment variables."""
    global _config
    _config = ConfigurationManager.from_environment()
    return _config
