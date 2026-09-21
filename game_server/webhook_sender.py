import requests
import time

WEBHOOK_URL = "http://localhost:9000/webhook/match-complete"

def fire_match_complete_webhook(match_id: str, winner: str, players: list):
    payload = {
        "event": "match_complete",
        "match_id": match_id,
        "winner": winner,
        "players": players,
        "timestamp": time.time()
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=5)
        print(f"Webhook sent. Status: {response.status_code}, Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Webhook failed: {e}")

if __name__ == "__main__":
    # Simulating a match that just ended
    fire_match_complete_webhook(
        match_id="match_001",
        winner="Alice",
        players=["Alice", "Bob"]
    )