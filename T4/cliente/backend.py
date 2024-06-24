import socket
import json

class ClientBackend:
    def __init__(self, config_path):
        with open(config_path, 'r') as config_file:
            self.config = json.load(config_file)
        self.client_socket = None

    def connect(self, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.config['host'], port))

    def send_message(self, message):
        self.client_socket.sendall(message.encode('utf-8'))
        response = self.client_socket.recv(4096).decode('utf-8')
        return response

    def close(self):
        if self.client_socket:
            self.client_socket.close()
