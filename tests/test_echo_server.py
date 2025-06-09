import socket
import threading
import time
from server.echo_server import EchoServer

def run_server():
    server = EchoServer()
    server.start()

def test_echo_response():
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    time.sleep(1)  # Wait for server to start

    with socket.create_connection(('127.0.0.1', 65432)) as sock:
        test_msg = b'Hello Echo'
        sock.sendall(test_msg)
        data = sock.recv(1024)
        assert data == test_msg
