import sys
from PyQt6.QtWidgets import QApplication
from frontend import ClientFrontend

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <puerto>")
        sys.exit(1)

    config_path = 'config.json'
    port = int(sys.argv[1])

    # Crear la aplicación antes de cualquier widget
    app = QApplication(sys.argv)
    
    client_frontend = ClientFrontend(config_path)
    client_frontend.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
