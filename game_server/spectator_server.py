import asyncio
import json
import redis
import websockets

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

connected_spectators = set()

async def handler(websocket):
    connected_spectators.add(websocket)
    print(f"Spectator connected. Total spectators: {len(connected_spectators)}")
    try:
        async for _ in websocket:
            pass  # spectators don't send anything, just listen
    finally:
        connected_spectators.discard(websocket)
        print(f"Spectator disconnected. Total spectators: {len(connected_spectators)}")

async def broadcast_loop():
    while True:
        keys = r.keys("player:*")
        state = {}
        for key in keys:
            x = float(r.hget(key, "x") or 0.0)
            y = float(r.hget(key, "y") or 0.0)
            state[key] = {"x": x, "y": y}

        if connected_spectators and state:
            message = json.dumps({"type": "state_update", "players": state})
            websockets.broadcast(connected_spectators, message)
            print(f"Broadcast to {len(connected_spectators)} spectator(s): {state}")

        await asyncio.sleep(0.5)

async def main():
    async with websockets.serve(handler, "localhost", 7000):
        print("Spectator WebSocket server running on ws://localhost:7000")
        await broadcast_loop()

if __name__ == "__main__":
    asyncio.run(main())