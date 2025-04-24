from kafka import KafkaProducer
import time
import json
from PollResponseAPI import PollResponseAPI 

producer = KafkaProducer(bootstrap_servers='localhost:9092')
topic = 'livepoll'
poll = PollResponseAPI()

print("🚀 Producer started. Sending messages to Kafka...\n(Press Ctrl+C to stop)")

try:
    while True:
        message = poll.poll_response_api()
        producer.send(topic, message.encode('utf-8'))
        print(f"📤 Sent: {message}")
        time.sleep(2)  
except KeyboardInterrupt:
    print("\n🛑 Stopping producer.")
finally:
    producer.flush()
    producer.close()
