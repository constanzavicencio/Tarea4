import socket
import json
import sys
from threading import Thread, Event

# Global event to signal server shutdown
shutdown_event = Event()

def handle_client(client_socket):
    try:
        while not shutdown_event.is_set():
            # Read message length
            raw_msglen = client_socket.recv(4)
            if not raw_msglen:
                break
            msglen = int.from_bytes(raw_msglen, 'big')
            
            # Sanity check for msglen
            if msglen <= 0 or msglen > 10**6:  # assuming 1MB is a reasonable upper limit for a message
                print(f"Invalid message length: {msglen}")
                break

            # Read the message data
            data = bytearray()
            while len(data) < msglen:
                packet = client_socket.recv(min(msglen - len(data), 4096))
                if not packet:
                    break
                data.extend(packet)
            
            # Process the message
            print(f"Received message: {data}")
            # Here you would add logic to process the message
            response = b'OK'
            client_socket.send(len(response).to_bytes(4, 'big') + response)
    except MemoryError:
        print("MemoryError: Message size is too large")
        shutdown_event.set()  # Signal server shutdown
    except ConnectionResetError:
        print("Client disconnected abruptly")
    finally:
        client_socket.close()

def main():
    # Read configuration
    with open('config.json') as f:
        config = json.load(f)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config['host'], int(sys.argv[1])))
    server.listen(5)
    print("Server listening on port", sys.argv[1])

    try:
        while not shutdown_event.is_set():
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr}")
            client_handler = Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    except KeyboardInterrupt:
        print("Server shutting down")
    finally:
        shutdown_event.set()  # Ensure all threads are aware of the shutdown
        server.close()

if __name__ == "__main__":
    main()
