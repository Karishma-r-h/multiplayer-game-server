import socket
from protocol import pack_packet, unpack_packet

HOST = "127.0.0.1"
PORT = 5000

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"UDP sequenced server listening on {HOST}:{PORT}")

    last_seq_seen = {}  # tracks the newest sequence number per client address

    while True:
        data, addr = sock.recvfrom(1024)
        seq_num, payload = unpack_packet(data)

        newest_seen = last_seq_seen.get(addr, -1)
        if seq_num <= newest_seen:
            print(f"Discarding stale packet #{seq_num} from {addr} (newest seen: {newest_seen})")
            continue

        last_seq_seen[addr] = seq_num
        print(f"Accepted packet #{seq_num} from {addr}: {payload}")

        # echo back the same sequence number and payload
        sock.sendto(pack_packet(seq_num, payload), addr)

if __name__ == "__main__":
    main()