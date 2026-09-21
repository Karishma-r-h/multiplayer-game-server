import socket
import time
from protocol import pack_packet, pack_position

HOST = "127.0.0.1"
PORT = 5000

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    x, y = 0.0, 0.0
    seq_num = 0

    print("Simulating player movement. Press Ctrl+C to stop.")
    try:
        while True:
            x += 1.0
            packet = pack_packet(seq_num, pack_position(x, y))
            sock.sendto(packet, (HOST, PORT))
            print(f"Sent seq #{seq_num}, position ({x:.1f}, {y:.1f})")
            seq_num += 1
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopped.")
    finally:
        sock.close()

if __name__ == "__main__":
    main()