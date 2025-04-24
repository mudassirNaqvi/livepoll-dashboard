from kafka.admin import KafkaAdminClient, NewTopic

admin_client = KafkaAdminClient(bootstrap_servers="localhost:9092", client_id='test_client')

topic_name = "livepoll"
num_partitions = 1
replication_factor = 1


new_topic = NewTopic(topic_name, num_partitions=num_partitions, replication_factor=replication_factor)


admin_client.create_topics([new_topic])


print(f"Topic '{topic_name}' created successfully!")


admin_client.close()
