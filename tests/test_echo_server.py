import threading
import time
import http.client
from server.echo_server import start_server

def run_server():
    start_server(port=8081)

def test_http_echo():
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1)

    conn = http.client.HTTPConnection("127.0.0.1", 8081)
    conn.request("GET", "/?echo_body=hello")
    response = conn.getresponse()
    body = response.read().decode()

    assert response.status == 200
    assert body == "hello"
