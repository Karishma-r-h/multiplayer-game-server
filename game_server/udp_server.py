import socket
from protocol import pack_packet, unpack_packet, pack_position, unpack_position

HOST = "127.0.0.1"
PORT = 5000

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"UDP position server listening on {HOST}:{PORT}")

    last_seq_seen = {}

    while True:
        data, addr = sock.recvfrom(1024)
        seq_num, payload = unpack_packet(data)

        newest_seen = last_seq_seen.get(addr, -1)
        if seq_num <= newest_seen:
            print(f"Discarding stale packet #{seq_num} from {addr}")
            continue

        last_seq_seen[addr] = seq_num
        x, y = unpack_position(payload)
        print(f"Player at {addr} -> seq #{seq_num}, position ({x:.1f}, {y:.1f})")

        sock.sendto(pack_packet(seq_num, pack_position(x, y)), addr)

if __name__ == "__main__":
    main()