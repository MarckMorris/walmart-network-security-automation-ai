"""
Symantec DLP Integration Client
Phase 3: Real integration ready for production
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class SymantecDLPClient:
    """Symantec Data Loss Prevention API Client"""

    def __init__(
        self, base_url: str, username: str, password: str, verify_ssl: bool = True
    ):
        """
        Initialize Symantec DLP client

        Args:
            base_url: DLP server URL (e.g., https://dlp.example.com)
            username: DLP admin username
            password: DLP admin password
            verify_ssl: Whether to verify SSL certificates
        """
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        self.token = None

        logger.info(f"Initialized Symantec DLP client for {base_url}")
        self._authenticate()

    def _authenticate(self) -> None:
        """Authenticate and get session token"""
        try:
            url = f"{self.base_url}/ProtectManager/webservices/v2/authentication/login"

            auth_data = {"username": self.username, "password": self.password}

            response = requests.post(url, json=auth_data, verify=self.verify_ssl)
            response.raise_for_status()

            self.token = response.json().get("token")
            self.session.headers.update(
                {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.token}",
                }
            )

            logger.info("Successfully authenticated with Symantec DLP")

        except requests.exceptions.RequestException as e:
            logger.error(f"Error authenticating with DLP: {e}")
            raise

    def get_incidents(
        self,
        severity: Optional[str] = None,
        status: Optional[str] = None,
        hours: int = 24,
    ) -> List[Dict]:
        """
        Get DLP incidents

        Args:
            severity: Filter by severity (LOW, MEDIUM, HIGH, CRITICAL)
            status: Filter by status (NEW, OPEN, RESOLVED)
            hours: Look back period in hours

        Returns:
            List of incidents
        """
        try:
            url = f"{self.base_url}/ProtectManager/webservices/v2/incidents"

            start_time = (datetime.utcnow() - timedelta(hours=hours)).isoformat()

            params = {"creation_date_later_than": start_time}

            if severity:
                params["severity"] = severity
            if status:
                params["status"] = status

            response = self.session.get(url, params=params, verify=self.verify_ssl)
            response.raise_for_status()

            return response.json().get("incidents", [])

        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting incidents: {e}")
            return []

    def get_incident_details(self, incident_id: int) -> Optional[Dict]:
        """Get detailed information about a specific incident"""
        try:
            url = (
                f"{self.base_url}/ProtectManager/webservices/v2/incidents/{incident_id}"
            )

            response = self.session.get(url, verify=self.verify_ssl)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting incident {incident_id}: {e}")
            return None

    def update_incident_status(
        self, incident_id: int, status: str, remediation_status: Optional[str] = None
    ) -> bool:
        """
        Update incident status

        Args:
            incident_id: Incident ID
            status: New status (NEW, OPEN, RESOLVED)
            remediation_status: Remediation status

        Returns:
            True if successful
        """
        try:
            url = (
                f"{self.base_url}/ProtectManager/webservices/v2/incidents/{incident_id}"
            )

            update_data = {"status": status}

            if remediation_status:
                update_data["remediation_status"] = remediation_status

            response = self.session.patch(url, json=update_data, verify=self.verify_ssl)
            response.raise_for_status()

            logger.info(f"Successfully updated incident {incident_id} to {status}")
            return True

        except requests.exceptions.RequestException as e:
            logger.error(f"Error updating incident {incident_id}: {e}")
            return False

    def create_policy(self, policy_data: Dict) -> Optional[int]:
        """Create a new DLP policy"""
        try:
            url = f"{self.base_url}/ProtectManager/webservices/v2/policies"

            response = self.session.post(url, json=policy_data, verify=self.verify_ssl)
            response.raise_for_status()

            policy_id = response.json().get("policy_id")
            logger.info(f"Successfully created policy {policy_id}")
            return policy_id

        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating policy: {e}")
            return None

    def get_policy_violations_summary(self, hours: int = 24) -> Dict:
        """Get summary of policy violations"""
        try:
            url = f"{self.base_url}/ProtectManager/webservices/v2/incidents/summary"

            start_time = (datetime.utcnow() - timedelta(hours=hours)).isoformat()

            params = {"creation_date_later_than": start_time, "group_by": "policy"}

            response = self.session.get(url, params=params, verify=self.verify_ssl)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting policy violations summary: {e}")
            return {}

    def quarantine_file(self, incident_id: int) -> bool:
        """Quarantine a file involved in an incident"""
        try:
            url = f"{self.base_url}/ProtectManager/webservices/v2/incidents/{incident_id}/remediate"

            remediation_data = {
                "action": "QUARANTINE",
                "reason": "Automated security response",
            }

            response = self.session.post(
                url, json=remediation_data, verify=self.verify_ssl
            )
            response.raise_for_status()

            logger.info(f"Successfully quarantined file from incident {incident_id}")
            return True

        except requests.exceptions.RequestException as e:
            logger.error(f"Error quarantining file for incident {incident_id}: {e}")
            return False
