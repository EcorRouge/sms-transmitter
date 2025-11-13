ARG SERVICE_HOST_VERSION=latest
FROM ecorrouge/rococo-service-host:${SERVICE_HOST_VERSION}

WORKDIR /app/src/services/sms_transmitter

# Copy poetry files
COPY pyproject.toml poetry.lock* ./

# Configure Poetry to install dependencies globally (no virtual environment)
RUN poetry config virtualenvs.create false

# Install ALL dependencies (main + dev) globally in the base image
RUN poetry install --no-root && \
    poetry cache clear --all pypi

COPY ./src ./src

WORKDIR /app

ENV PYTHONPATH=/app

ENV MESSAGING_TYPE=RabbitMqConnection
ENV PROCESSOR_TYPE=SmsServiceProcessor
ENV PROCESSOR_MODULE=services.sms_transmitter.src.sms_processor

COPY ./docker-entrypoint.sh ./
RUN chmod +x ./docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh", "-l", "-c"]
