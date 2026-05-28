# Kafka topic으로 JSON 메시지를 전송하는 producer 과제입니다.
from kafka import KafkaProducer
from datetime import datetime, timedelta
import json
import random
import time

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

base_time = datetime.now() - timedelta(minutes=5)
event_types = [
    "checkout_completed",
    "payment_authorized",
    "cart_abandoned",
    "refund_requested",
    "delivery_status_changed",
]

for i in range(30):
    offset_minutes = random.randint(0, 4)
    offset_seconds = random.randint(0, 59)
    msg_time = base_time + timedelta(minutes=offset_minutes, seconds=offset_seconds)

    message = {
        "id": i + 1,
        "message": random.choice(event_types),
        "timestamp": msg_time.strftime("%Y-%m-%d %H:%M:%S")
    }

    producer.send("test-topic", message)
    print(f"전송된 메시지: {message}")
    time.sleep(0.5)

producer.flush()
