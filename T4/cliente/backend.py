import socket
import json

class ClientBackend:
    def __init__(self, config_path):
        self.load_config(config_path)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def load_config(self, config_path):
        with open(config_path) as f:
            self.config = json.load(f)

    def connect(self, port):
        self.client_socket.connect((self.config['host'], port))

    def encode_message(self, message):
        msglen = len(message)
        encoded_message = msglen.to_bytes(4, 'big')
        encoded_message += message.encode('utf-8')
        return encoded_message

    def send_message(self, message):
        encoded_msg = self.encode_message(message)
        self.client_socket.send(encoded_msg)
        raw_msglen = self.client_socket.recv(4)
        if not raw_msglen:
            return None
        msglen = int.from_bytes(raw_msglen, 'big')
        response = self.client_socket.recv(msglen)
        return response.decode('utf-8')

    def close(self):
        self.client_socket.close()
