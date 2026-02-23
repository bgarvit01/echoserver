"""
Enhanced CLI interface for the Echo Server.

Provides a clean command-line interface with validation and better organization.
"""

import argparse
import sys
from typing import Optional

from server.config import (
    ServerConfig, ConfigurationManager, LogLevel, LogFormat,
    TimingControls, FeatureFlags, LoggingConfig, CommandConfig
)
from server.echo_server import EchoServer
from server.utils.network_utils import NetworkUtils


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Start an HTTP Echo Server with comprehensive features",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python run_server.py
  
  # Custom host and port  
  python run_server.py --host 0.0.0.0 --port 8080
  
  # Structured logging with timing limits
  python run_server.py --log-format object --max-delay 30000
  
  # Disable certain features for security
  python run_server.py --disable-file-ops --disable-host-info
        """
    )
    
    # Server configuration
    server_group = parser.add_argument_group('Server Configuration')
    server_group.add_argument(
        '--host', type=str, default='127.0.0.1',
        help='Host to bind to (default: 127.0.0.1)'
    )
    server_group.add_argument(
        '--port', type=int, default=80,
        help='Port to listen on (default: 80)'
    )
    server_group.add_argument(
        '--enable-http2', action='store_true',
        help='Enable HTTP/2 support (requires hypercorn)'
    )
    
    # Timing controls
    timing_group = parser.add_argument_group('Timing Controls')
    timing_group.add_argument(
        '--min-delay', type=int, default=0,
        help='Minimum delay time in milliseconds (default: 0)'
    )
    timing_group.add_argument(
        '--max-delay', type=int, default=60000,
        help='Maximum delay time in milliseconds (default: 60000)'
    )
    
    # Logging configuration
    logging_group = parser.add_argument_group('Logging Configuration')
    logging_group.add_argument(
        '--log-level', type=str, default='debug',
        choices=[level.value for level in LogLevel],
        help='Log level (default: debug)'
    )
    logging_group.add_argument(
        '--log-format', type=str, default='default',
        choices=[fmt.value for fmt in LogFormat],
        help='Log format (default: default)'
    )
    logging_group.add_argument(
        '--log-app-name', type=str, default='echoserver',
        help='Application name for logs (default: echoserver)'
    )
    
    # Feature toggles
    features_group = parser.add_argument_group('Feature Toggles')
    features_group.add_argument(
        '--disable-logs', action='store_true',
        help='Disable request logging'
    )
    features_group.add_argument(
        '--disable-host-info', action='store_true',
        help='Disable host information in response'
    )
    features_group.add_argument(
        '--disable-http-info', action='store_true',
        help='Disable HTTP information in response'
    )
    features_group.add_argument(
        '--disable-request-info', action='store_true',
        help='Disable request information in response'
    )
    features_group.add_argument(
        '--disable-cookies', action='store_true',
        help='Disable cookie parsing'
    )
    features_group.add_argument(
        '--disable-file-ops', action='store_true',
        help='Disable file operations'
    )
    features_group.add_argument(
        '--disable-custom-headers', action='store_true',
        help='Disable custom headers'
    )
    features_group.add_argument(
        '--enable-env-vars', action='store_true',
        help='Enable environment variables in response (security sensitive)'
    )
    
    # Utility options
    parser.add_argument(
        '--config-check', action='store_true',
        help='Check configuration and exit without starting server'
    )
    parser.add_argument(
        '--show-config', action='store_true',
        help='Show current configuration and exit'
    )
    parser.add_argument(
        '--version', action='version', version='Echo Server 2.0.0 (Refactored)'
    )
    
    return parser


def validate_args(args, network_utils: NetworkUtils) -> None:
    """Validate parsed arguments."""
    # Validate host
    if not network_utils.is_valid_host(args.host):
        raise ValueError(f"Invalid host: {args.host}")
    
    # Validate port
    if not network_utils.is_valid_port(args.port):
        raise ValueError(f"Invalid port: {args.port}. Must be between 1 and 65535.")
    
    # Validate timing
    if args.min_delay < 0:
        raise ValueError("Minimum delay cannot be negative")
    
    if args.max_delay < args.min_delay:
        raise ValueError("Maximum delay must be >= minimum delay")
    
    if args.max_delay > 300000:  # 5 minutes
        raise ValueError("Maximum delay cannot exceed 5 minutes (300000ms)")


def create_config_from_args(args) -> ServerConfig:
    """Create ServerConfig from parsed command line arguments."""
    # Start with environment-based config
    config = ConfigurationManager.from_environment()
    
    # Override with command line arguments
    config.host = args.host
    config.port = args.port
    config.enable_http2 = args.enable_http2
    
    # Timing configuration
    config.timing = TimingControls(
        min_delay_ms=args.min_delay,
        max_delay_ms=args.max_delay
    )
    
    # Logging configuration
    config.logging = LoggingConfig(
        app_name=args.log_app_name,
        level=LogLevel(args.log_level),
        format=LogFormat(args.log_format)
    )
    
    # Feature flags
    features = FeatureFlags(
        enable_logs=not args.disable_logs,
        enable_host=not args.disable_host_info,
        enable_http=not args.disable_http_info,
        enable_request=not args.disable_request_info,
        enable_cookies=not args.disable_cookies,
        enable_file=not args.disable_file_ops,
        enable_header=not args.disable_custom_headers,
        enable_env=args.enable_env_vars
    )
    config.features = features
    
    return config


def print_configuration(config: ServerConfig) -> None:
    """Print current configuration in a readable format."""
    print("═" * 60)
    print("Echo Server Configuration")
    print("═" * 60)
    
    print(f"Server:")
    print(f"  Host: {config.host}")
    print(f"  Port: {config.port}")
    protocol = "HTTP/2" if config.enable_http2 else "HTTP/1.1"
    print(f"  Protocol: {protocol}")
    print(f"  URL: http://{config.host}:{config.port}")
    print(f"  Instance ID: {config.instance_id}")
    
    print(f"\nLogging:")
    print(f"  Level: {config.logging.level.value}")
    print(f"  Format: {config.logging.format.value}")
    print(f"  App Name: {config.logging.app_name}")
    
    print(f"\nTiming:")
    print(f"  Min Delay: {config.timing.min_delay_ms}ms")
    print(f"  Max Delay: {config.timing.max_delay_ms}ms")
    
    print(f"\nFeatures:")
    print(f"  Logging: {'✓' if config.features.enable_logs else '✗'}")
    print(f"  Host Info: {'✓' if config.features.enable_host else '✗'}")
    print(f"  HTTP Info: {'✓' if config.features.enable_http else '✗'}")
    print(f"  Request Info: {'✓' if config.features.enable_request else '✗'}")
    print(f"  Cookies: {'✓' if config.features.enable_cookies else '✗'}")
    print(f"  File Ops: {'✓' if config.features.enable_file else '✗'}")
    print(f"  Custom Headers: {'✓' if config.features.enable_header else '✗'}")
    print(f"  Environment Vars: {'✓' if config.features.enable_env else '✗'}")
    
    print(f"\nCustom Commands:")
    print(f"  Body Query: ?{config.commands.http_body_query}=value")
    print(f"  Body Header: {config.commands.http_body_header}: value")
    print(f"  Code Query: ?{config.commands.http_code_query}=200-404-500")
    print(f"  Code Header: {config.commands.http_code_header}: 404")
    print(f"  Time Query: ?{config.commands.time_query}=5000")
    print(f"  Time Header: {config.commands.time_header}: 5000")
    
    if config.features.enable_file:
        print(f"  File Query: ?{config.commands.file_query}=/path")
        print(f"  File Header: {config.commands.file_header}: /path")
    
    print("═" * 60)


def main() -> None:
    """Main entry point for the CLI."""
    try:
        # Parse command line arguments
        parser = create_argument_parser()
        args = parser.parse_args()
        
        # Validate arguments
        network_utils = NetworkUtils()
        validate_args(args, network_utils)
        
        # Create configuration
        config = create_config_from_args(args)
        
        # Handle utility commands
        if args.show_config or args.config_check:
            print_configuration(config)
            
            if args.config_check:
                print("✓ Configuration is valid")
            
            sys.exit(0)
        
        # Print startup information
        print_configuration(config)
        print("\nStarting server...")
        
        # Start server
        server = EchoServer(config)
        server.start()
        
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
