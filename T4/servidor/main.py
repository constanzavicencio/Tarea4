import socket
import json
import sys
from threading import Thread, Event

shutdown_event = Event()

def handle_client(client_socket):
    try:
        while not shutdown_event.is_set():
            raw_msglen = client_socket.recv(4)
            if not raw_msglen:
                break
            msglen = int.from_bytes(raw_msglen, 'big')
            
            if msglen <= 0 or msglen > 10**6:  
                print(f"Largo de mensaje inválido: {msglen}")
                break
            
            data = bytearray()
            while len(data) < msglen:
                packet = client_socket.recv(min(msglen - len(data), 4096))
                if not packet:
                    break
                data.extend(packet)
            
            print(f"Mensaje recibido: {data.decode('utf-8')}")
            response = b'OK'
            client_socket.send(len(response).to_bytes(4, 'big') + response)
    except MemoryError:
        print("MemoryError: El largo del mensaje es muy grande")
        shutdown_event.set()
    except ConnectionResetError:
        print("Cliente desconectado")
    finally:
        client_socket.close()

def main():
    # Read configuration
    with open('config.json') as f:
        config = json.load(f)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config['host'], int(sys.argv[1])))
    server.listen(5)
    print("Servidor conectado al puerto ", sys.argv[1])

    try:
        while not shutdown_event.is_set():
            client_socket, addr = server.accept()
            print(f"Conexión aceptada de {addr}")
            client_handler = Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    except KeyboardInterrupt:
        print("El servidor se ha desconectado")
    finally:
        shutdown_event.set()  
        server.close()

if __name__ == "__main__":
    main()
