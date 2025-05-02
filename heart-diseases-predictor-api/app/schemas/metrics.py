from prometheus_client import Counter, Histogram, Summary, Gauge
import time

# Define Prometheus metrics
REQUEST_COUNT = Counter(
    'api_requests_total',
    'Total number of API requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'api_request_latency_seconds',
    'Request latency in seconds',
    ['method', 'endpoint'],
    buckets=[0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0]
)

PREDICTION_LATENCY = Histogram(
    'prediction_latency_seconds',
    'Time to generate prediction',
    ['outcome'],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5]
)

MODEL_PREDICTION_COUNTER = Counter(
    'model_predictions_total',
    'Total number of model predictions',
    ['outcome']
)

ACTIVE_REQUESTS = Gauge(
    'api_active_requests',
    'Number of active requests'
)

# Custom metric to track input data distributions
AGE_SUMMARY = Summary(
    'patient_age_summary',
    'Summary statistics for patient age'
)

# Function to track prediction metrics
def track_prediction(result, start_time):
    latency = time.time() - start_time
    outcome = "survive" if "will survive" in result else "not_survive"
    PREDICTION_LATENCY.labels(outcome=outcome).observe(latency)
    MODEL_PREDICTION_COUNTER.labels(outcome=outcome).inc()
    return result

# Function to track age distribution
def track_age(age):
    AGE_SUMMARY.observe(age)