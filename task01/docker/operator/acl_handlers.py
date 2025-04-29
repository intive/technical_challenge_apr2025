import kopf
from kafka.admin import KafkaAdminClient, ACL, ResourcePattern, ACLOperation, ACLPermissionType, ResourceType, ACLResourcePatternType
from config import get_kafka_config

def build_acl(spec):
    resource_pattern = ResourcePattern(
        resource_type=getattr(ResourceType, spec.get('resourceType', 'TOPIC').upper()),
        resource_name=spec['resourceName'],
        pattern_type=getattr(ACLResourcePatternType, spec.get('patternType', 'LITERAL').upper())
    )
    acl = ACL(
        resource_pattern=resource_pattern,
        principal=spec['principal'],
        host=spec.get('host', '*'),
        operation=getattr(ACLOperation, spec['operation'].upper()),
        permission_type=getattr(ACLPermissionType, spec.get('permissionType', 'ALLOW').upper())
    )
    return acl

@kopf.on.create('intive.com', 'v1', 'kafkaacls')
def create_fn(spec, name, body, **kwargs):
    admin = KafkaAdminClient(**get_kafka_config())
    acl   = build_acl(spec)

    try:
        admin.create_acls([acl])
        kopf.event(body, type="Normal", reason="KafkaAclCreated",
                   message=f"Kafka ACL has been created: '{name}'")
    except Exception as e:
        kopf.exception(body, reason="KafkaAclError",
                       message=f"Failed to create Kafka ACL: {e}'")
        raise

@kopf.on.delete('intive.com', 'v1', 'kafkaacls')
def delete_fn(spec, name, body, **kwargs):
    admin = KafkaAdminClient(**get_kafka_config())
    acl   = build_acl(spec)

    try:
        admin.delete_acls([acl])
        kopf.event(body, type="Normal", reason="KafkaAclDeleted",
                   message=f"Kafka ACL has been deleted: '{name}'")        
    except Exception as e:
        kopf.event(body, type="Warning", reason="KafkaAclError",
                       message=f"Failed to delete Kafka ACL: {e}'")
        raise

