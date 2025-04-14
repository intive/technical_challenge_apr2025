FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY rds_operator.py .

CMD ["kopf", "run", "--standalone", "--verbose", "rds_operator.py"]
