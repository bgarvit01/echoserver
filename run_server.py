import argparse
from server.echo_server import start_server

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start an HTTP Echo Server.")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on")
    args = parser.parse_args()

    start_server(port=args.port)
