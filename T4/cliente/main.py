import sys
from frontend import ClientFrontend
from PyQt6.QtWidgets import QApplication

def main():
    if len(sys.argv) < 2:
        sys.exit(1)
    
    port = int(sys.argv[1])

    app = QApplication(sys.argv)
    frontend = ClientFrontend("config.json", port)
    frontend.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
