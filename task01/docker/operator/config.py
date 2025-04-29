import os

def get_kafka_config():
    config = {
        'bootstrap_servers': os.environ.get('KAFKA_BOOTSTRAP', 'localhost:9094'),
        'security_protocol': "SSL",
        **({'ssl_cafile': os.environ["KAFKA_CA_CERT"]} if "KAFKA_CA_CERT" in os.environ else {}),
        'ssl_certfile': os.environ.get("KAFKA_CLIENT_CERT", "/certs/client.crt"),
        'ssl_keyfile': os.environ.get("KAFKA_CLIENT_KEY", "/certs/client.key")
    }
    return config
