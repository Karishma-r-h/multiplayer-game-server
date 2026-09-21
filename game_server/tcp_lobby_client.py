import socket
import sys

HOST = "127.0.0.1"
PORT = 6000

def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "Player"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    print(sock.recv(1024).decode().strip())
    sock.sendall(f"JOIN {name}\n".encode())

    while True:
        data = sock.recv(1024)
        if not data:
            break
        print(data.decode().strip())

if __name__ == "__main__":
    main()