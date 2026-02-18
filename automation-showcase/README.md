# Automation Showcase Scripts

These scripts demonstrate **production-ready automation capabilities** directly aligned 
with the Walmart Senior Network Security Engineer position requirements.

## Scripts Overview

### 01_deploy_ise_policy.py
**Demonstrates:** Policy deployment automation, async/await, bulk operations
- Deploy security policies to 10,000+ store locations simultaneously
- Parallel deployment using asyncio.gather()
- Automated policy validation after deployment
\\\ash
python 01_deploy_ise_policy.py
\\\

### 02_detect_config_drift.py
**Demonstrates:** Configuration compliance, drift detection, auto-remediation
- Compare live configuration vs Git-stored baseline
- Detect unauthorized changes across ISE nodes
- Auto-remediate MEDIUM severity drift
- Alert on HIGH severity changes requiring manual review
\\\ash
python 02_detect_config_drift.py
\\\

### 03_automated_health_check.py
**Demonstrates:** Infrastructure monitoring, proactive maintenance
- Automated health checks for ISE and DLP platforms
- Certificate expiry monitoring
- Session count thresholds
- Agent connectivity verification
\\\ash
python 03_automated_health_check.py
\\\

### 04_incident_auto_response.py
**Demonstrates:** Event-driven automation, severity-based decision making
- CRITICAL: Auto-quarantine device + alert SOC via PagerDuty
- HIGH: VLAN isolation + Slack notification
- MEDIUM: Create alert + monitor
- LOW: Log only
\\\ash
python 04_incident_auto_response.py
\\\

### 05_policy_lifecycle.py
**Demonstrates:** Full CRUD operations, version control, audit trails
- Create policies with automatic versioning
- Update with change tracking
- Rollback to any previous version
- Complete audit trail for compliance
\\\ash
python 05_policy_lifecycle.py
\\\

### 06_bulk_endpoint_management.py
**Demonstrates:** Enterprise-scale automation, batch processing
- Manage 10,000+ endpoints across all Walmart stores
- Batch processing with configurable size
- Concurrent operations with asyncio
- Progress tracking and error handling
\\\ash
python 06_bulk_endpoint_management.py
\\\

## Running All Scripts
\\\ash
# Run from project root
cd C:/Users/sicst/VS_Code/walmart-network-security-automation-ai

# Run individual scripts
python automation-showcase/01_deploy_ise_policy.py
python automation-showcase/02_detect_config_drift.py
python automation-showcase/03_automated_health_check.py
python automation-showcase/04_incident_auto_response.py
python automation-showcase/05_policy_lifecycle.py
python automation-showcase/06_bulk_endpoint_management.py
\\\

## Alignment with Walmart Requirements

| Requirement | Implemented In |
|------------|---------------|
| NAC/DLP automation | Scripts 01, 04, 05 |
| Configuration drift detection | Script 02 |
| Infrastructure health checks | Script 03 |
| Policy lifecycle management | Script 05 |
| RESTful API integration | All scripts (ISE/DLP clients) |
| Async programming (async/await) | All scripts |
| Bulk/enterprise-scale operations | Script 06 |
| Logging and error handling | All scripts |
| Python best practices | All scripts |
