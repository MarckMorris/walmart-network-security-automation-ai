# Operations Guide

## Monitoring

### Grafana Dashboards

Access Grafana at http://localhost:3000 (local) or production endpoint.

**Default Credentials**: admin/admin

**Available Dashboards**:
- Network Security Overview
- ML Model Performance
- System Resources
- Security Incidents

### Prometheus Metrics

Access Prometheus at http://localhost:9090

**Key Metrics**:
- `anomalies_detected_total`: Total anomalies detected
- `security_incidents_total`: Security incidents by severity
- `remediation_actions_total`: Remediation actions executed
- `ml_inference_duration_seconds`: ML inference latency

## Maintenance

### Database Maintenance

```bash
# Backup database
docker exec walmart-netsec-postgres pg_dump -U postgres network_security_automation > backup.sql

# Restore database
docker exec -i walmart-netsec-postgres psql -U postgres network_security_automation < backup.sql
```

### Model Retraining

```bash
# Generate new training data
python scripts/data_generation/generate_synthetic_data.py

# Retrain models
python -m src.ml.training.trainer
```

### Log Management

Logs are stored in:
- Application logs: `logs/application.log`
- Container logs: `docker compose logs <service>`

## Backup and Recovery

### Backup Procedures

1. **Database**: Daily automated backups
2. **ML Models**: Version controlled in Azure Blob Storage
3. **Configuration**: Git version control

### Recovery Procedures

1. **Database Recovery**:
   ```bash
   # Restore from backup
   psql -U postgres network_security_automation < backup.sql
   ```

2. **Service Recovery**:
   ```bash
   # Restart services
   docker compose restart
   
   # Or rebuild
   docker compose up -d --build
   ```

## Security Operations

### Incident Response

1. **Alert Triggered** → Check Grafana dashboard
2. **Investigate** → Review logs and metrics
3. **Remediate** → Execute manual remediation if needed
4. **Document** → Update incident log

### Access Management

- API access: OAuth2 tokens (production)
- Database access: Least privilege principle
- Azure resources: RBAC roles

## Performance Optimization

### Database Tuning

```sql
-- Optimize query performance
VACUUM ANALYZE network_events;

-- Check index usage
SELECT * FROM pg_stat_user_indexes;
```

### Application Tuning

- Adjust worker processes in docker-compose.yml
- Configure Redis cache TTL
- Optimize ML batch sizes
