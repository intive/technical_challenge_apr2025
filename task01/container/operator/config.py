import os

def get_kafka_config():
    config = {
        'bootstrap_servers': os.environ.get('KAFKA_BOOTSTRAP', 'localhost:9094'),
        'security_protocol': os.environ.get('KAFKA_SECURITY_PROTOCOL', 'SASL_SSL'),
        'ssl_cafile': os.environ.get('KAFKA_CA_CERT', '/certs/ca.crt'),
        'sasl_mechanism': os.environ.get('KAFKA_SASL_MECHANISM', 'SCRAM-SHA-512'),
        'sasl_plain_username': os.environ.get('KAFKA_SASL_USERNAME', ''),
        'sasl_plain_password': os.environ.get('KAFKA_SASL_PASSWORD', '')
    }
    return config
