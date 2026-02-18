from fastapi import Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Definir métricas
anomalies_detected = Counter('anomalies_detected_total', 'Total anomalies detected')
api_requests = Counter('api_requests_total', 'Total API requests', ['method', 'endpoint'])
request_duration = Histogram('request_duration_seconds', 'Request duration')

def get_metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
