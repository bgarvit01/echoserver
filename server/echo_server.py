import socket
import logging

logging.basicConfig(level=logging.INFO)

class EchoServer:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port

    def start(self):
        logging.info(f"Starting echo server on {self.host}:{self.port}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            logging.info("Server is listening for connections...")

            while True:
                conn, addr = s.accept()
                logging.info(f"Connected by {addr}")
                with conn:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        logging.info(f"Received: {data}")
                        conn.sendall(data)
