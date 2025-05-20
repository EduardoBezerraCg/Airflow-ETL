# Dockerfile
FROM apache/airflow:2.10.5

USER root

# Copy requirements.txt into the image
COPY requirements.txt /

# Install Python dependencies
RUN pip install --no-cache-dir -r /requirements.txt

# Install the Spark provider for Airflow
RUN pip install --no-cache-dir apache-airflow-providers-apache-spark

USER airflow