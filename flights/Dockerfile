# # Use the official Python 3.8 image as the base image
# FROM python:3.8-slim-buster

# # Set the working directory inside the container
# WORKDIR /python-docker

# # Copy the requirements file into the container
# COPY requirements.txt requirements.txt

# # Install the required dependencies
# RUN pip3 install -r requirements.txt

# # Copy the rest of your application code into the container
# COPY . .

# # Expose port 5001
# EXPOSE 5001

# # Specify the command to run your Flask app
# CMD ["opentelemetry-instrument", "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5001"]


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
