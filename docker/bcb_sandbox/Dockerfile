FROM system1-sandbox:v2
USER root
RUN pip install --no-cache-dir Faker==37.11.0 pytz==2025.2
COPY worker.py /opt/sandbox/bcb_worker.py
USER sandbox
WORKDIR /tmp
