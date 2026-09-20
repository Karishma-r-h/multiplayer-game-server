import socket

HOST = "127.0.0.1"
PORT = 5000

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = b"hello server"
    sock.sendto(message, (HOST, PORT))
    data, _ = sock.recvfrom(1024)
    print(f"Server replied: {data}")

if __name__ == "__main__":
    main()