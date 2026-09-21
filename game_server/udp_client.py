import socket
import time
import random
from protocol import pack_packet, unpack_packet, pack_position, unpack_position

HOST = "127.0.0.1"
PORT = 5000
PACKET_LOSS_RATE = 0.2

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)

    predicted_x, predicted_y = 0.0, 0.0
    seq_num = 0
    pending_inputs = {}

    print("Simulating client-side prediction with reconciliation. Runs 40 ticks.")
    try:
        for _ in range(40):
            dx, dy = 1.0, 0.0
            predicted_x += dx
            predicted_y += dy
            pending_inputs[seq_num] = (dx, dy)

            if random.random() > PACKET_LOSS_RATE:
                sock.sendto(pack_packet(seq_num, pack_position(dx, dy)), (HOST, PORT))
            else:
                print(f"  (simulated: input #{seq_num} lost in transit)")

            print(f"Tick {seq_num}: predicted position = ({predicted_x:.1f}, {predicted_y:.1f})")
            seq_num += 1

            while True:
                try:
                    data, _ = sock.recvfrom(1024)
                except (BlockingIOError, OSError):
                    break  # no data waiting right now -- normal, keep going

                acked_seq, payload = unpack_packet(data)
                server_x, server_y = unpack_position(payload)

                pending_inputs = {s: v for s, v in pending_inputs.items() if s > acked_seq}

                if abs(server_x - predicted_x) > 0.01 or abs(server_y - predicted_y) > 0.01:
                    print(f"  CORRECTION: server says ({server_x:.1f}, {server_y:.1f}) "
                          f"after ack #{acked_seq}, but we predicted ({predicted_x:.1f}, {predicted_y:.1f})")

                predicted_x, predicted_y = server_x, server_y
                for s in sorted(pending_inputs):
                    rdx, rdy = pending_inputs[s]
                    predicted_x += rdx
                    predicted_y += rdy

                print(f"  Reconciled position after ack #{acked_seq}: ({predicted_x:.1f}, {predicted_y:.1f})")

            time.sleep(0.1)
    finally:
        sock.close()
        print("Done.")

if __name__ == "__main__":
    main()