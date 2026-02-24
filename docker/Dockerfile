FROM apache/airflow:2.9.3-python3.10

USER root
COPY requirements.txt /requirements.txt
RUN chmod 644 /requirements.txt

USER airflow
RUN python -m pip install --no-cache-dir -r /requirements.txt \
  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.3/constraints-3.10.txt"
