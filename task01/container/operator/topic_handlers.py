import kopf
from kafka.admin import KafkaAdminClient, NewTopic
from config import get_kafka_config

@kopf.on.create('intive.com', 'v1', 'kafkatopics')
def create_topic(spec, name, body, **kwargs):
    admin = KafkaAdminClient(**get_kafka_config())
    topic = NewTopic(
        name=name,
        num_partitions=spec.get('partitions', 1),
        replication_factor=spec.get('replicationFactor', 1),
        topic_configs=spec.get('config', {})
    )
    try:
        admin.create_topics([topic])
        kopf.event(body, type="Normal", reason="KafkaTopicCreated",
                   message=f"Kafka Topic has been created: '{name}'")        
    except Exception as e:
        kopf.exception(body, reason="KafkaTopicError",
                       message=f"Failed to create Kafka Topic: {e}'")        
        raise 

@kopf.on.delete('intive.com', 'v1', 'kafkatopics')
def delete_topic(name, body, **kwargs):
    admin = KafkaAdminClient(**get_kafka_config())
    try:
        admin.delete_topics([name])
        kopf.event(body, type="Normal", reason="KafkaTopicDeleted",
                   message=f"Kafka Topic has been deleted: '{name}'")      
    except Exception as e:
        kopf.event(body, type="Warning", reason="KafkaTopicError",
                       message=f"Failed to delete Kafka Topic: {e}'")
