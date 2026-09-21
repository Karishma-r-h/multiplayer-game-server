import socket
import threading

HOST = "127.0.0.1"
PORT = 6000
REQUIRED_PLAYERS = 2

clients = []  # list of (conn, addr, name)
lock = threading.Lock()

def handle_client(conn, addr):
    conn.sendall(b"Connected. Send: JOIN <your_name>\n")
    data = conn.recv(1024).decode().strip()

    if not data.startswith("JOIN "):
        conn.sendall(b"Expected JOIN <name>. Disconnecting.\n")
        conn.close()
        return

    name = data.split(" ", 1)[1]
    with lock:
        clients.append((conn, addr, name))
        print(f"{name} joined from {addr}. Lobby size: {len(clients)}/{REQUIRED_PLAYERS}")
        current_count = len(clients)

    if current_count < REQUIRED_PLAYERS:
        conn.sendall(f"Waiting for players... ({current_count}/{REQUIRED_PLAYERS})\n".encode())
    else:
        with lock:
            names = [c[2] for c in clients]
            print(f"Lobby full: {names}. Starting match!")
            for c_conn, _, _ in clients:
                c_conn.sendall(f"START match=[{','.join(names)}]\n".encode())
            clients.clear()

def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen()
    print(f"TCP lobby server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server_sock.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()