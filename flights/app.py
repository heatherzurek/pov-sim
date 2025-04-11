from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger
from utils import get_random_int

# --- OpenTelemetry Metrics Setup ---
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.metrics import get_meter_provider, set_meter_provider
from opentelemetry.sdk.resources import Resource

# --- Configure OpenTelemetry ---
resource = Resource.create(attributes={
    "service.name": "flights",
    "service.namespace": "flights-service",
    "service.version": "1.0.0",
})

exporter = OTLPMetricExporter(endpoint="http://alloy:4317", insecure=True)
reader = PeriodicExportingMetricReader(exporter)
provider = MeterProvider(resource=resource, metric_readers=[reader])
set_meter_provider(provider)  # Must come before get_meter_provider

# --- Create the meter and counter ---
meter = get_meter_provider().get_meter("flights")
request_counter = meter.create_counter(
    name="flights_http_requests_total",
    unit="1",
    description="Total HTTP requests received by the flights service"
)

# --- Flask Setup ---
app = Flask(__name__)
Swagger(app)
CORS(app)

@app.before_request
def before_request():
    request_counter.add(1, {
        "http.method": request.method,
        "http.path": request.path
    })

@app.route('/health', methods=['GET'])
def health():
    """Health endpoint
    ---
    responses:
      200:
        description: Returns healthy
    """
    return jsonify({"status": "healthy"}), 200

@app.route("/", methods=['GET'])
def home():
    """No-op home endpoint
    ---
    responses:
      200:
        description: Returns ok
    """
    return jsonify({"message": "ok"}), 200

@app.route("/flights/<airline>", methods=["GET"])
def get_flights(airline):
    """Get flights endpoint. Optionally, set raise to trigger an exception.
    ---
    parameters:
      - name: airline
        in: path
        type: string
        enum: ["AA", "UA", "DL"]
        required: true
      - name: raise
        in: query
        type: string
        enum: ["500"]
        required: false
    responses:
      200:
        description: Returns a list of flights for the selected airline
    """
    if request.args.get("raise"):
        raise Exception("Triggered error")  # pylint: disable=broad-exception-raised
    return jsonify({airline: [get_random_int(100, 999)]}), 200

@app.route("/flight", methods=["POST"])
def book_flight():
    """Book flights endpoint. Optionally, set raise to trigger an exception.
    ---
    parameters:
      - name: passenger_name
        in: query
        type: string
        enum: ["John Doe", "Jane Doe"]
        required: true
      - name: flight_num
        in: query
        type: string
        enum: ["101", "202", "303", "404", "505", "606"]
        required: true
      - name: raise
        in: query
        type: string
        enum: ["500"]
        required: false
    responses:
      200:
        description: Booked a flight for the selected passenger and flight_num
    """
    if request.args.get("raise"):
        raise Exception("Triggered error")  # pylint: disable=broad-exception-raised

    passenger_name = request.args.get("passenger_name")
    flight_num = request.args.get("flight_num")
    booking_id = get_random_int(100, 999)
    return jsonify({
        "passenger_name": passenger_name,
        "flight_num": flight_num,
        "booking_id": booking_id
    }), 200

if __name__ == "__main__":
    app.run(debug=False, port=5001, host="0.0.0.0")
