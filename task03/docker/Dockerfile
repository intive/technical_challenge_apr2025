FROM python:3.13.3-slim

RUN addgroup --system --gid 1000 k8s_operator_grp && \
    adduser --system --uid 1000 --ingroup k8s_operator_grp k8s_operator_usr

WORKDIR /operator

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY rds_operator.py .

RUN chown -R k8s_operator_usr:k8s_operator_grp /operator

USER k8s_operator_usr

ENV PYTHONUNBUFFERED=1

CMD ["kopf", "run", "--standalone", "--verbose", "rds_operator.py"]