# API Reference

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Currently no authentication (development mode). Production will use OAuth2.

## Endpoints

### Health Check

**GET** `/health`

Returns system health status.

**Response**:
```json
{
  "status": "healthy",
  "service": "Network Security Automation",
  "version": "1.0.0"
}
```

### Anomaly Detection

**POST** `/anomaly/detect`

Detect anomalies in network events.

**Request**:
```json
{
  "events": [
    {
      "source_ip": "10.1.1.100",
      "bytes_sent": 1000000,
      ...
    }
  ],
  "threshold": 0.1
}
```

**Response**:
```json
{
  "anomalies_detected": 5,
  "total_events": 100,
  "anomaly_rate": 0.05,
  "results": [...]
}
```

### Recent Anomalies

**GET** `/anomaly/recent?hours=24&limit=100`

Get recent anomaly detections.

**Response**:
```json
{
  "anomalies": [...],
  "count": 10,
  "time_range_hours": 24
}
```
