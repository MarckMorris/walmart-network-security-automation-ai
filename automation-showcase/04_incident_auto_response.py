import asyncio
from typing import Dict, List
from datetime import datetime
from enum import Enum
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IncidentSeverity(Enum):
    CRITICAL = "CRITICAL"
    HIGH     = "HIGH"
    MEDIUM   = "MEDIUM"
    LOW      = "LOW"


class IncidentResponseAutomation:
    """
    Automated incident response system.
    CRITICAL -> quarantine + SOC alert
    HIGH     -> VLAN isolation + team notify
    MEDIUM   -> alert + log
    LOW      -> log only
    """

    def __init__(self):
        self.response_log = []

    async def process_incident(self, incident: Dict) -> Dict:
        """Process incident and trigger automated response based on severity"""
        severity = IncidentSeverity(incident.get("severity", "LOW"))
        response = {
            "incident_id": incident["id"],
            "severity": severity.value,
            "actions_taken": [],
            "timestamp": datetime.now().isoformat()
        }

        if severity == IncidentSeverity.CRITICAL:
            logger.warning(f"CRITICAL: {incident['id']} - Initiating quarantine")
            response["actions_taken"] = [
                {"action": "QUARANTINE_DEVICE", "target": incident.get("source_ip"), "status": "EXECUTED"},
                {"action": "QUARANTINE_FILE",   "target": incident.get("file_path", "N/A"), "status": "EXECUTED"},
                {"action": "ALERT_SOC",         "channel": "PagerDuty", "status": "SENT"}
            ]
        elif severity == IncidentSeverity.HIGH:
            logger.warning(f"HIGH: {incident['id']} - VLAN isolation")
            response["actions_taken"] = [
                {"action": "ISOLATE_VLAN",  "vlan_id": 999, "status": "EXECUTED"},
                {"action": "NOTIFY_TEAM",   "channel": "Slack", "status": "SENT"}
            ]
        elif severity == IncidentSeverity.MEDIUM:
            response["actions_taken"] = [
                {"action": "CREATE_ALERT", "status": "CREATED"}
            ]
        else:
            response["actions_taken"] = [
                {"action": "LOG_INCIDENT", "status": "LOGGED"}
            ]

        self.response_log.append(response)
        return response


async def main():
    print("=" * 80)
    print("AUTOMATED INCIDENT RESPONSE - WALMART DEMO")
    print("=" * 80)
    print()

    responder = IncidentResponseAutomation()

    incidents = [
        {"id": "INC-001", "severity": "CRITICAL", "type": "Data Exfiltration",  "source_ip": "10.1.24.156", "file_path": "/data/customers.xlsx"},
        {"id": "INC-002", "severity": "HIGH",     "type": "Policy Violation",   "source_ip": "10.1.18.92"},
        {"id": "INC-003", "severity": "MEDIUM",   "type": "Suspicious Transfer","source_ip": "10.1.32.78"},
        {"id": "INC-004", "severity": "LOW",      "type": "Policy Warning",     "source_ip": "10.1.45.23"}
    ]

    for incident in incidents:
        print(f"Incident: {incident['id']} | {incident['severity']} | {incident['type']} | {incident['source_ip']}")
        response = await responder.process_incident(incident)
        for action in response["actions_taken"]:
            print(f"  -> {action['action']}: {action['status']}")
        print()

    print("=" * 80)
    print(f"Processed {len(incidents)} incidents autonomously")
    critical = sum(1 for i in incidents if i["severity"] == "CRITICAL")
    high     = sum(1 for i in incidents if i["severity"] == "HIGH")
    print(f"  CRITICAL: {critical} auto-quarantined | HIGH: {high} VLAN-isolated")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())