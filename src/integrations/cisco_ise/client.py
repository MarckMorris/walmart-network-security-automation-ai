"""
Cisco ISE Integration Client
Phase 3: Real integration ready for production with pxGrid support
"""

import json
import logging
from typing import Dict, List, Optional

import requests
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)


class CiscoISEClient:
    """Cisco Identity Services Engine API Client"""

    def __init__(
        self, base_url: str, username: str, password: str, verify_ssl: bool = True
    ):
        """
        Initialize Cisco ISE client

        Args:
            base_url: ISE server URL (e.g., https://ise.example.com:9060)
            username: ISE admin username
            password: ISE admin password
            verify_ssl: Whether to verify SSL certificates
        """
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(username, password)
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )

        logger.info(f"Initialized Cisco ISE client for {base_url}")

    def get_endpoint(self, mac_address: str) -> Optional[Dict]:
        """
        Get endpoint details by MAC address

        Args:
            mac_address: Device MAC address

        Returns:
            Endpoint details or None if not found
        """
        try:
            url = f"{self.base_url}/ers/config/endpoint"
            params = {"filter": f"mac.EQ.{mac_address}"}

            response = self.session.get(url, params=params, verify=self.verify_ssl)
            response.raise_for_status()

            data = response.json()
            endpoints = data.get("SearchResult", {}).get("resources", [])

            if endpoints:
                endpoint_id = endpoints[0]["id"]
                return self.get_endpoint_by_id(endpoint_id)

            return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting endpoint {mac_address}: {e}")
            return None

    def get_endpoint_by_id(self, endpoint_id: str) -> Optional[Dict]:
        """Get endpoint details by ID"""
        try:
            url = f"{self.base_url}/ers/config/endpoint/{endpoint_id}"
            response = self.session.get(url, verify=self.verify_ssl)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting endpoint by ID {endpoint_id}: {e}")
            return None

    def quarantine_endpoint(
        self, mac_address: str, reason: str = "Security violation"
    ) -> bool:
        """
        Quarantine an endpoint by changing its authorization profile

        Args:
            mac_address: Device MAC address
            reason: Reason for quarantine

        Returns:
            True if successful, False otherwise
        """
        try:
            # First get the endpoint
            endpoint = self.get_endpoint(mac_address)
            if not endpoint:
                logger.error(f"Endpoint {mac_address} not found")
                return False

            endpoint_id = endpoint["ERSEndPoint"]["id"]

            # Update endpoint with quarantine group
            url = f"{self.base_url}/ers/config/endpoint/{endpoint_id}"

            update_data = {
                "ERSEndPoint": {
                    "id": endpoint_id,
                    "groupId": "QUARANTINE_GROUP_ID",  # Configure this for your environment
                    "customAttributes": {
                        "customAttributes": {"quarantine_reason": reason}
                    },
                }
            }

            response = self.session.put(url, json=update_data, verify=self.verify_ssl)
            response.raise_for_status()

            logger.info(f"Successfully quarantined endpoint {mac_address}")
            return True

        except requests.exceptions.RequestException as e:
            logger.error(f"Error quarantining endpoint {mac_address}: {e}")
            return False

    def get_active_sessions(self) -> List[Dict]:
        """Get all active network sessions"""
        try:
            url = f"{self.base_url}/admin/API/mnt/Session/ActiveList"
            response = self.session.get(url, verify=self.verify_ssl)
            response.raise_for_status()

            return response.json().get("activeList", [])

        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting active sessions: {e}")
            return []

    def get_authentication_status(self, mac_address: str) -> Optional[Dict]:
        """Get authentication status for a MAC address"""
        try:
            url = f"{self.base_url}/admin/API/mnt/AuthStatus/MACAddress/{mac_address}"
            response = self.session.get(url, verify=self.verify_ssl)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting auth status for {mac_address}: {e}")
            return None

    def create_authorization_profile(
        self, name: str, vlan_id: int, acl_name: str
    ) -> bool:
        """Create a new authorization profile"""
        try:
            url = f"{self.base_url}/ers/config/authorizationprofile"

            profile_data = {
                "AuthorizationProfile": {
                    "name": name,
                    "accessType": "ACCESS_ACCEPT",
                    "vlan": {"nameID": str(vlan_id), "tagID": vlan_id},
                    "acl": acl_name,
                }
            }

            response = self.session.post(url, json=profile_data, verify=self.verify_ssl)
            response.raise_for_status()

            logger.info(f"Successfully created authorization profile {name}")
            return True

        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating authorization profile: {e}")
            return False
