"""
Cisco ISE Simulator
Phase 3: Mock ISE REST API for local testing
"""

import random
import uuid
from datetime import datetime

from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock data store
endpoints = {}
sessions = {}


def generate_mac():
    """Generate random MAC address"""
    return ":".join(["%02x" % random.randint(0, 255) for _ in range(6)])


# Initialize some mock endpoints
for i in range(10):
    mac = generate_mac()
    endpoints[mac] = {
        "id": str(uuid.uuid4()),
        "mac": mac,
        "name": f"Device-{i}",
        "groupId": "STANDARD_GROUP",
        "ipAddress": f"10.1.{random.randint(1, 254)}.{random.randint(1, 254)}",
        "profileId": "Employee-Profile",
        "status": "CONNECTED",
        "lastSeen": datetime.utcnow().isoformat(),
    }


@app.route("/ers/config/endpoint", methods=["GET"])
def list_endpoints():
    """List all endpoints"""
    mac_filter = request.args.get("filter", "")

    if "mac.EQ." in mac_filter:
        mac = mac_filter.split("mac.EQ.")[1]
        if mac in endpoints:
            return jsonify(
                {
                    "SearchResult": {
                        "resources": [
                            {"id": endpoints[mac]["id"], "name": endpoints[mac]["name"]}
                        ]
                    }
                }
            )
        return jsonify({"SearchResult": {"resources": []}}), 404

    return jsonify(
        {
            "SearchResult": {
                "resources": [
                    {"id": ep["id"], "name": ep["name"]} for ep in endpoints.values()
                ]
            }
        }
    )


@app.route("/ers/config/endpoint/<endpoint_id>", methods=["GET"])
def get_endpoint(endpoint_id):
    """Get endpoint by ID"""
    for ep in endpoints.values():
        if ep["id"] == endpoint_id:
            return jsonify({"ERSEndPoint": ep})
    return jsonify({"error": "Endpoint not found"}), 404


@app.route("/ers/config/endpoint/<endpoint_id>", methods=["PUT"])
def update_endpoint(endpoint_id):
    """Update endpoint (for quarantine)"""
    for mac, ep in endpoints.items():
        if ep["id"] == endpoint_id:
            data = request.json
            if "ERSEndPoint" in data:
                endpoints[mac].update(data["ERSEndPoint"])
            return jsonify({"success": True})
    return jsonify({"error": "Endpoint not found"}), 404


@app.route("/admin/API/mnt/Session/ActiveList", methods=["GET"])
def get_active_sessions():
    """Get active sessions"""
    active = []
    for mac, ep in endpoints.items():
        if ep["status"] == "CONNECTED":
            active.append(
                {
                    "mac_address": mac,
                    "ip_address": ep["ipAddress"],
                    "username": f"user_{mac.replace(':', '')}",
                    "session_start": datetime.utcnow().isoformat(),
                }
            )
    return jsonify({"activeList": active})


@app.route("/admin/API/mnt/AuthStatus/MACAddress/<mac>", methods=["GET"])
def get_auth_status(mac):
    """Get authentication status"""
    if mac in endpoints:
        return jsonify(
            {
                "mac_address": mac,
                "authenticated": True,
                "authorization_profile": endpoints[mac]["profileId"],
                "auth_method": "802.1X",
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
    return jsonify({"error": "MAC not found"}), 404


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "service": "ISE Simulator",
            "endpoints_count": len(endpoints),
        }
    )


if __name__ == "__main__":
    print("Starting Cisco ISE Simulator on port 9060...")
    app.run(host="0.0.0.0", port=9060, debug=True)
