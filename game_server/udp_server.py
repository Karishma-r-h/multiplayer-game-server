import socket
import redis
from protocol import pack_packet, unpack_packet, pack_position, unpack_position
from kafka_producer import publish_event

HOST = "127.0.0.1"
PORT = 5000

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def get_position(addr_key: str) -> tuple[float, float]:
    x = float(r.hget(addr_key, "x") or 0.0)
    y = float(r.hget(addr_key, "y") or 0.0)
    return x, y

def set_position(addr_key: str, x: float, y: float):
    r.hset(addr_key, mapping={"x": x, "y": y})

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"UDP server (Redis-backed) listening on {HOST}:{PORT}")

    last_seq_seen = {}

    while True:
        data, addr = sock.recvfrom(1024)
        seq_num, payload = unpack_packet(data)
        addr_key = f"player:{addr[0]}:{addr[1]}"

        newest_seen = last_seq_seen.get(addr, -1)
        if seq_num <= newest_seen:
            print(f"Discarding stale input #{seq_num} from {addr}")
            continue
        last_seq_seen[addr] = seq_num

        dx, dy = unpack_position(payload)

        x, y = get_position(addr_key)
        x += dx
        y += dy
        set_position(addr_key, x, y)

        print(f"Applied input #{seq_num} from {addr}: delta=({dx:.1f},{dy:.1f}) -> "
              f"authoritative (Redis)=({x:.1f},{y:.1f})")

        if seq_num % 10 == 0:
            publish_event("player_moved", {"addr": addr_key, "x": x, "y": y, "seq": seq_num})

        ack_packet = pack_packet(seq_num, pack_position(x, y))
        sock.sendto(ack_packet, addr)

if __name__ == "__main__":
    main()