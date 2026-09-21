import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "game-events",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

print("Analytics consumer listening for game events...")
for message in consumer:
    print(f"[Analytics] Received: {message.value}")