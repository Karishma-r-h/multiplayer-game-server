import json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def publish_event(event_type: str, data: dict):
    event = {"type": event_type, **data}
    producer.send("game-events", value=event)
    producer.flush()
    print(f"Published event to Kafka: {event}")