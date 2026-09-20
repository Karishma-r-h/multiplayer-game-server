import socket
import time
from protocol import pack_packet, unpack_packet

HOST = "127.0.0.1"
PORT = 5000

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Deliberately send sequence numbers out of order: 1, 2, then a late 1-again style packet (seq 0)
    test_sequence = [
        (1, b"move_up"),
        (2, b"move_right"),
        (0, b"move_left"),   # arrives late/out of order, should be discarded
        (3, b"jump"),
    ]

    for seq_num, payload in test_sequence:
        packet = pack_packet(seq_num, payload)
        sock.sendto(packet, (HOST, PORT))
        time.sleep(0.2)  # small delay so server prints are readable in order sent

    sock.close()

if __name__ == "__main__":
    main()