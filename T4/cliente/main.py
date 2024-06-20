import sys
from frontend import ClientFrontend

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <puerto>")
        sys.exit(1)

    config_path = 'config.json'
    port = int(sys.argv[1])
    client_frontend = ClientFrontend(config_path)
    client_frontend.start(port)

if __name__ == "__main__":
    main()
