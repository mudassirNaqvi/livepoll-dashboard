# livepoll-dashboard

# Live Poll Dashboard using Kafka & Streamlit

This dashboard displays live poll responses received through Apache Kafka.

## Features
- Real-time consumer of Kafka messages
- Live charts and response table
- Lightweight and mobile-friendly layout

## Requirements
- Python 3.x
- Kafka running on localhost
- Streamlit
- kafka-python
- pandas

## How to Run
1. Start Kafka and Zookeeper
2. Run `python producer.py` to send messages
3. Run the dashboard:

```bash
streamlit run dashboard.py
