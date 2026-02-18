# Deployment Guide

## Local Development Deployment

### 1. Prerequisites
- Docker Desktop installed and running
- Python 3.13+ installed
- 8GB RAM minimum

### 2. Setup Steps

```bash
# Initialize project
python setup_master.py

# Configure environment
cp .env.example .env

# Install dependencies
pip install -r requirements.txt

# Generate training data
python scripts/data_generation/generate_synthetic_data.py

# Start services
docker compose up -d

# Check status
docker compose ps
```

### 3. Verify Deployment

```bash
# Test API
curl http://localhost:8000/api/v1/health

# Run tests
pytest tests/
```

## Production Deployment (Azure)

### 1. Prerequisites
- Azure subscription with appropriate permissions
- Azure CLI installed and configured
- Terraform 1.5+
- kubectl installed

### 2. Infrastructure Deployment

```bash
cd terraform

# Initialize
terraform init

# Configure variables
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars

# Plan
terraform plan

# Apply
terraform apply
```

### 3. Application Deployment

```bash
# Get AKS credentials
az aks get-credentials --resource-group walmart-netsec-prod-rg --name walmart-netsec-prod-aks

# Deploy with Ansible
ansible-playbook ansible/playbooks/deploy_production.yml

# Verify deployment
kubectl get pods -n walmart-netsec
```

### 4. Post-Deployment

```bash
# Check pod status
kubectl get pods -n walmart-netsec

# View logs
kubectl logs -f deployment/netsec-automation -n walmart-netsec

# Check service endpoints
kubectl get svc -n walmart-netsec
```

## Troubleshooting

### Local Development

**Issue**: PostgreSQL won't start
```bash
docker compose down -v
docker compose up -d postgres
docker compose logs postgres
```

**Issue**: API not responding
```bash
docker compose logs app
```

### Production

**Issue**: Pods not starting
```bash
kubectl describe pod <pod-name> -n walmart-netsec
kubectl logs <pod-name> -n walmart-netsec
```

**Issue**: Database connection failed
```bash
# Check database status
az postgres flexible-server show --resource-group walmart-netsec-prod-rg --name <server-name>
```
