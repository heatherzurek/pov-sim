FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENV OTEL_SERVICE_NAME=flask-app
ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://host.docker.internal:4317
ENV OTEL_EXPORTER_OTLP_PROTOCOL=grpc

EXPOSE 5001

ENV FLASK_APP=app.py

CMD ["opentelemetry-instrument", "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5001"]
