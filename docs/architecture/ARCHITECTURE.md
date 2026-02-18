# Architecture Documentation

## System Overview

The Walmart Network Security Automation AI platform is a distributed, cloud-native system designed for autonomous network security operations.

## Components

### 1. Data Layer
- **PostgreSQL + TimescaleDB**: Time-series network event storage
- **Redis**: Caching and real-time data

### 2. ML Layer
- **Anomaly Detection**: Isolation Forest model
- **Time-Series Prediction**: LSTM model
- **Inference Engine**: Real-time ML predictions

### 3. Integration Layer
- **Cisco ISE Client**: Network access control
- **Symantec DLP Client**: Data loss prevention
- **Azure Services**: Cloud integration

### 4. Automation Layer
- **Remediation Engine**: Autonomous response orchestration
- **Policy Management**: Dynamic policy updates

### 5. API Layer
- **FastAPI**: RESTful API
- **WebSocket**: Real-time updates

### 6. Observability
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **Logging**: Structured logging

## Data Flow

1. Network events → PostgreSQL/TimescaleDB
2. ML Engine analyzes events
3. Anomalies detected → Remediation Engine
4. Remediation actions executed via integrations
5. Metrics exported to Prometheus
6. Visualization in Grafana

## Security

- TLS everywhere
- Azure Key Vault for secrets
- RBAC for all services
- Audit logging

## Scalability

- Horizontal scaling via Kubernetes
- Database read replicas
- Caching layer with Redis
- Async processing

## High Availability

- Multi-AZ deployment
- Database replication
- Load balancing
- Health checks and auto-recovery
