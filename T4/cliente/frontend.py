from backend import ClientBackend

class ClientFrontend:
    def __init__(self, config_path):
        self.backend = ClientBackend(config_path)

    def start(self, port):
        try:
            self.backend.connect(port)
            print(f"Conectado al servidor en el puerto {port}")
            while True:
                msg = input("Ingrese mensaje: ")
                if msg.lower() == "salir":
                    break
                response = self.backend.send_message(msg)
                if response is None:
                    print("Servidor desconectado")
                    break
                print("Respuesta del servidor:", response)
        except KeyboardInterrupt:
            print("Cliente cerrando")
        finally:
            self.backend.close()
