# Start from a minimal Python image
FROM python:3.13.3-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /certs && \
    mkdir -p /app

RUN addgroup --system --gid 1000 k8s_operator_grp && \
    adduser --system --uid 1000 --ingroup k8s_operator_grp k8s_operator_usr && \
    mkdir -p /operator /certs && \
    chown -R k8s_operator_usr:k8s_operator_grp /operator /certs

WORKDIR /operator

COPY operator/ .

ENTRYPOINT ["kopf", "run", "--standalone", "main.py"]