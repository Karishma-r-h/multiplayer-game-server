import socket
import time
import random
from protocol import pack_packet, unpack_packet, pack_position, unpack_position

HOST = "127.0.0.1"
PORT = 5000
PACKET_LOSS_RATE = 0.2  # simulate 20% of inputs never reaching the server

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)  # so we can check for server replies without freezing the loop

    predicted_x, predicted_y = 0.0, 0.0
    seq_num = 0
    pending_inputs = {}  # seq_num -> (dx, dy): sent but not yet confirmed by the server

    print("Simulating client-side prediction with reconciliation. Runs 40 ticks.")
    try:
        for _ in range(40):
            # 1. Sample input for this tick (always "move right 1 unit")
            dx, dy = 1.0, 0.0

            # 2. PREDICT: apply it locally immediately, don't wait for the server
            predicted_x += dx
            predicted_y += dy
            pending_inputs[seq_num] = (dx, dy)

            # 3. Send to server (simulate loss)
            if random.random() > PACKET_LOSS_RATE:
                sock.sendto(pack_packet(seq_num, pack_position(dx, dy)), (HOST, PORT))
            else:
                print(f"  (simulated: input #{seq_num} lost in transit)")

            print(f"Tick {seq_num}: predicted position = ({predicted_x:.1f}, {predicted_y:.1f})")
            seq_num += 1

            # 4. RECONCILE: process any server acknowledgements that have arrived
            try:
                while True:
                    data, _ = sock.recvfrom(1024)
                    acked_seq, payload = unpack_packet(data)
                    server_x, server_y = unpack_position(payload)

                    # drop every input the server has already accounted for
                    pending_inputs = {s: v for s, v in pending_inputs.items() if s > acked_seq}

                    if abs(server_x - predicted_x) > 0.01 or abs(server_y - predicted_y) > 0.01:
                        print(f"  CORRECTION: server says ({server_x:.1f}, {server_y:.1f}) "
                              f"after ack #{acked_seq}, but we predicted ({predicted_x:.1f}, {predicted_y:.1f})")

                    # snap to server truth, then replay whatever inputs are still unconfirmed
                    predicted_x, predicted_y = server_x, server_y
                    for s in sorted(pending_inputs):
                        rdx, rdy = pending_inputs[s]
                        predicted_x += rdx
                        predicted_y += rdy

                    print(f"  Reconciled position after ack #{acked_seq}: ({predicted_x:.1f}, {predicted_y:.1f})")
            except BlockingIOError:
                pass  # no server data waiting right now, that's fine

            time.sleep(0.1)
    finally:
        sock.close()
        print("Done.")

if __name__ == "__main__":
    main()