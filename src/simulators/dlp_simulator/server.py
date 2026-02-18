"""
Symantec DLP Simulator
Phase 3: Mock DLP REST API for local testing
"""

import random
import uuid
from datetime import datetime, timedelta

from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock session token
SESSION_TOKEN = str(uuid.uuid4())

# Mock incidents store
incidents = []

# Initialize some mock incidents
SEVERITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
STATUSES = ["NEW", "OPEN", "RESOLVED"]
POLICY_NAMES = [
    "PCI Data Protection",
    "PII Detection",
    "Confidential Documents",
    "Source Code Protection",
]

for i in range(20):
    incident_id = 1000 + i
    incidents.append(
        {
            "incident_id": incident_id,
            "severity": random.choice(SEVERITIES),
            "status": random.choice(STATUSES),
            "policy_name": random.choice(POLICY_NAMES),
            "detection_date": (
                datetime.utcnow() - timedelta(hours=random.randint(1, 48))
            ).isoformat(),
            "user": f"user{random.randint(1, 100)}@walmart.com",
            "source": random.choice(["Email", "Endpoint", "Network", "Cloud"]),
            "destination": random.choice(
                ["External Email", "USB Drive", "Cloud Storage", "File Share"]
            ),
            "matched_data_type": random.choice(
                ["Credit Card", "SSN", "Confidential", "Source Code"]
            ),
            "match_count": random.randint(1, 50),
        }
    )


@app.route("/ProtectManager/webservices/v2/authentication/login", methods=["POST"])
def login():
    """Authentication endpoint"""
    return jsonify({"token": SESSION_TOKEN, "expires_in": 3600})


@app.route("/ProtectManager/webservices/v2/incidents", methods=["GET"])
def get_incidents():
    """Get DLP incidents"""
    severity_filter = request.args.get("severity")
    status_filter = request.args.get("status")

    filtered = incidents

    if severity_filter:
        filtered = [inc for inc in filtered if inc["severity"] == severity_filter]
    if status_filter:
        filtered = [inc for inc in filtered if inc["status"] == status_filter]

    return jsonify({"incidents": filtered, "total_count": len(filtered)})


@app.route(
    "/ProtectManager/webservices/v2/incidents/<int:incident_id>", methods=["GET"]
)
def get_incident_details(incident_id):
    """Get incident details"""
    for incident in incidents:
        if incident["incident_id"] == incident_id:
            return jsonify(incident)
    return jsonify({"error": "Incident not found"}), 404


@app.route(
    "/ProtectManager/webservices/v2/incidents/<int:incident_id>", methods=["PATCH"]
)
def update_incident(incident_id):
    """Update incident status"""
    for incident in incidents:
        if incident["incident_id"] == incident_id:
            data = request.json
            if "status" in data:
                incident["status"] = data["status"]
            if "remediation_status" in data:
                incident["remediation_status"] = data["remediation_status"]
            return jsonify({"success": True, "incident": incident})
    return jsonify({"error": "Incident not found"}), 404


@app.route(
    "/ProtectManager/webservices/v2/incidents/<int:incident_id>/remediate",
    methods=["POST"],
)
def remediate_incident(incident_id):
    """Remediate incident (quarantine, block, etc.)"""
    for incident in incidents:
        if incident["incident_id"] == incident_id:
            data = request.json
            incident["remediation_action"] = data.get("action", "QUARANTINE")
            incident["remediation_date"] = datetime.utcnow().isoformat()
            incident["status"] = "RESOLVED"
            return jsonify({"success": True, "incident": incident})
    return jsonify({"error": "Incident not found"}), 404


@app.route("/ProtectManager/webservices/v2/incidents/summary", methods=["GET"])
def get_incidents_summary():
    """Get incidents summary"""
    summary_by_policy = {}
    summary_by_severity = {}

    for incident in incidents:
        # By policy
        policy = incident["policy_name"]
        if policy not in summary_by_policy:
            summary_by_policy[policy] = {"count": 0, "severities": {}}
        summary_by_policy[policy]["count"] += 1

        severity = incident["severity"]
        if severity not in summary_by_policy[policy]["severities"]:
            summary_by_policy[policy]["severities"][severity] = 0
        summary_by_policy[policy]["severities"][severity] += 1

        # By severity
        if severity not in summary_by_severity:
            summary_by_severity[severity] = 0
        summary_by_severity[severity] += 1

    return jsonify(
        {
            "by_policy": summary_by_policy,
            "by_severity": summary_by_severity,
            "total_incidents": len(incidents),
        }
    )


@app.route("/ProtectManager/webservices/v2/policies", methods=["POST"])
def create_policy():
    """Create new DLP policy"""
    data = request.json
    policy_id = random.randint(1000, 9999)

    return (
        jsonify(
            {
                "policy_id": policy_id,
                "name": data.get("name", "New Policy"),
                "created_at": datetime.utcnow().isoformat(),
            }
        ),
        201,
    )


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "service": "DLP Simulator",
            "incidents_count": len(incidents),
        }
    )


if __name__ == "__main__":
    print("Starting Symantec DLP Simulator on port 8080...")
    app.run(host="0.0.0.0", port=8080, debug=True)
