import socket

HOST = "127.0.0.1"
PORT = 5000

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"UDP echo server listening on {HOST}:{PORT}")

    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received {data} from {addr}")
        sock.sendto(data, addr)

if __name__ == "__main__":
    main()