import kopf
import boto3
import base64
import random
import string
import traceback
from kubernetes import client, config

def generate_password(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@kopf.on.create('intive.com', 'v1', 'rdsinstances')
def create_fn(spec, name, namespace, body, **kwargs):
    db_name = spec.get('dbName')
    instance_type = spec.get('instanceType', 'db.t3.micro')
    engine = spec.get('engine', 'postgres')
    stage = spec.get('stage', 'dev')
    username = spec.get('username', 'admin')
    password_secret = spec.get('passwordSecretRef', f"{name}-credentials")
    region = spec.get('region', 'eu-central-1') 

    config.load_incluster_config()
    k8s = client.CoreV1Api()

    # Step 1: Generate password and create secret
    try:
        password = generate_password()
        secret = client.V1Secret(
            metadata=client.V1ObjectMeta(name=password_secret, namespace=namespace),
            string_data={
                "username": username,
                "password": password
            }
        )
        k8s.create_namespaced_secret(namespace=namespace, body=secret)
        kopf.event(body, type="Normal", reason="SecretCreated",
                   message=f"Credentials stored in secret '{password_secret}'")
    except Exception as e:
        error_msg = f"Failed to create Kubernetes secret: {str(e)}"
        kopf.exception(body, reason="SecretError", message=error_msg)
        raise

    # Step 2: Create RDS instance
    try:
        rds = boto3.client('rds', region_name=region)
        rds.create_db_instance(
            DBInstanceIdentifier=f"{name}-{stage}",
            MasterUsername=username,
            MasterUserPassword=password,
            DBInstanceClass=instance_type,
            Engine=engine,
            AllocatedStorage=20
        )

        msg = f"AWS RDS instance '{name}-{stage}' provisioning started."
        kopf.event(body, type="Normal", reason="RDSProvisioning", message=msg)

    except Exception as e:
        error_msg = f"Failed to create RDS instance: {str(e)}"
        kopf.exception(body, reason="RDSFailure", message=error_msg)
        raise

    return {"rds-instance": f"{name}-{stage}"}


@kopf.on.delete('intive.com', 'v1', 'rdsinstances')
def delete_fn(spec, name, namespace, body, **kwargs):
    stage = spec.get('stage', 'dev')
    password_secret = spec.get('passwordSecretRef', f"{name}-credentials")
    region = spec.get('region', 'eu-central-1')
    try:
        rds = boto3.client('rds', region_name=region)
        db_instance_id = f"{name}-{stage}"
        rds.delete_db_instance(
            DBInstanceIdentifier=db_instance_id,
            # For testing purposes we are not going to keep data, 
            # this shoulde be False or configurable.
            SkipFinalSnapshot=True
        )
        msg = f"RDS instance '{db_instance_id}' deletion initiated."
        kopf.event(body, type="Normal", reason="RDSDeletion", message=msg)
    except Exception as e:
        msg = f"Failed to delete RDS instance: {e}"
        kopf.event(body, type="Warning", reason="RDSDeletionFailed", message=msg)

    try:
        config.load_incluster_config()
        k8s = client.CoreV1Api()
        k8s.delete_namespaced_secret(name=password_secret, namespace=namespace)
        msg = f"Secret '{password_secret}' deleted."
        kopf.event(body, type="Normal", reason="SecretDeleted", message=msg)
    except client.exceptions.ApiException as e:
        if e.status == 404:
            msg = f"Secret '{password_secret}' already deleted."
        else:
            msg = f"Failed to delete secret: {e}"
        kopf.event(body, type="Warning", reason="SecretDeletionFailed", message=msg)