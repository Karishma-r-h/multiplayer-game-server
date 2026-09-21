import socket
from protocol import pack_packet, unpack_packet, pack_position, unpack_position

HOST = "127.0.0.1"
PORT = 5000

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"UDP prediction server listening on {HOST}:{PORT}")

    player_state = {}   # addr -> {"x": float, "y": float}  (authoritative)
    last_seq_seen = {}  # addr -> int

    while True:
        data, addr = sock.recvfrom(1024)
        seq_num, payload = unpack_packet(data)

        newest_seen = last_seq_seen.get(addr, -1)
        if seq_num <= newest_seen:
            print(f"Discarding stale input #{seq_num} from {addr}")
            continue
        last_seq_seen[addr] = seq_num

        dx, dy = unpack_position(payload)  # this payload is an INPUT delta, not absolute position

        state = player_state.setdefault(addr, {"x": 0.0, "y": 0.0})
        state["x"] += dx
        state["y"] += dy

        print(f"Applied input #{seq_num} from {addr}: delta=({dx:.1f},{dy:.1f}) -> "
              f"authoritative=({state['x']:.1f},{state['y']:.1f})")

        # ack: seq_num = which input this confirms, payload = authoritative position
        ack_packet = pack_packet(seq_num, pack_position(state["x"], state["y"]))
        sock.sendto(ack_packet, addr)

if __name__ == "__main__":
    main()