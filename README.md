![Logo](img/logo.png)

# Overview

This repository contains responses to the tasks provided in the offer.
Each task is located in its respective directory:

## Tasks

### task01
A Kubernetes Custom Resource Definition (CRD) was created using the `kopf-python` and `kafka-python` libraries. The CRD manages Kafka ACL and topic creation and deletion, with the assumption that once created, the resources are immutable.

### task02
A FluxCD configuration was developed with tenant isolation and per-team notifications through PagerDuty and Rocket.Chat. [Read more](task02/README.md)

### task03
A Kubernetes Custom Resource Definition (CRD) was developed for the creation of AWS RDS instances. For each RDS instance, a Kubernetes Secret is created to securely store the database username and password, using the `kopf`, `kubernetes`, and `boto3` Python libraries.

### task04
An OpenTelemetry (OTEL) configuration providing tenant isolation within the Grafana stack was developed, based on the FluxCD configuration from Task 02. [Read more](task04/README.md)
