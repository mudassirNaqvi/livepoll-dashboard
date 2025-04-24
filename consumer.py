# consumer.py
from kafka import KafkaConsumer
from helper import process_message 

consumer = KafkaConsumer(
    'livepoll', 
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest', 
    enable_auto_commit=True,
    group_id='my-group'
)

print("🟢 Listening for messages...")

for msg in consumer:
    text = msg.value.decode('utf-8')
    process_message(text)
