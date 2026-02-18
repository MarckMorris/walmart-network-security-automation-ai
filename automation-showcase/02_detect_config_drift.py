import asyncio
from typing import Dict, List
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConfigurationDriftDetector:
    """Detect and report configuration drift from baseline"""

    def __init__(self):
        self.baseline_configs = {}

    def load_baseline(self, device_id: str) -> Dict:
        """Load baseline configuration for comparison"""
        return {
            "device_id": device_id,
            "settings": {
                "authentication_enabled": True,
                "radius_server": "10.1.1.100",
                "session_timeout": 3600,
                "quarantine_vlan": 999,
                "allowed_protocols": ["802.1X", "MAB"]
            },
            "version": "1.0.0"
        }

    async def get_current_config(self, device_id: str) -> Dict:
        """Retrieve current configuration from ISE"""
        logger.info(f"Fetching current config for: {device_id}")
        return {
            "device_id": device_id,
            "settings": {
                "authentication_enabled": True,
                "radius_server": "10.1.1.100",
                "session_timeout": 7200,
                "quarantine_vlan": 998,
                "allowed_protocols": ["802.1X", "MAB", "WebAuth"]
            },
            "version": "1.0.0"
        }

    def detect_drift(self, baseline: Dict, current: Dict) -> Dict:
        """Compare baseline vs current and identify drift"""
        drifts = []
        for key in baseline["settings"]:
            if key not in current["settings"]:
                drifts.append({
                    "field": key,
                    "expected": baseline["settings"][key],
                    "actual": "MISSING",
                    "severity": "HIGH"
                })
            elif baseline["settings"][key] != current["settings"][key]:
                drifts.append({
                    "field": key,
                    "expected": baseline["settings"][key],
                    "actual": current["settings"][key],
                    "severity": "MEDIUM"
                })
        return {
            "device_id": baseline["device_id"],
            "has_drift": len(drifts) > 0,
            "drift_count": len(drifts),
            "drifts": drifts,
            "checked_at": datetime.now().isoformat()
        }

    async def auto_remediate(self, drift_report: Dict) -> bool:
        """Automatically remediate configuration drift"""
        for drift in drift_report["drifts"]:
            if drift["severity"] == "MEDIUM":
                logger.info(f"Auto-remediating: {drift['field']} -> {drift['expected']}")
            elif drift["severity"] == "HIGH":
                logger.warning(f"HIGH severity - Manual review required: {drift['field']}")
        return True


async def main():
    print("=" * 80)
    print("CONFIGURATION DRIFT DETECTION - WALMART DEMO")
    print("=" * 80)
    print()

    detector = ConfigurationDriftDetector()
    device_id = "ISE-Node-Dallas-01"

    baseline = detector.load_baseline(device_id)
    print(f"Baseline loaded (version {baseline['version']})")

    current = await detector.get_current_config(device_id)
    print("Current configuration retrieved")
    print()

    drift_report = detector.detect_drift(baseline, current)

    if drift_report["has_drift"]:
        print(f"DRIFT DETECTED: {drift_report['drift_count']} configuration(s) differ")
        print()
        for drift in drift_report["drifts"]:
            print(f"  [{drift['severity']}] Field: {drift['field']}")
            print(f"        Expected: {drift['expected']}")
            print(f"        Actual:   {drift['actual']}")
            print()
        print("Initiating auto-remediation...")
        await detector.auto_remediate(drift_report)
    else:
        print("No drift detected - Configuration compliant with baseline")

    print()
    print("=" * 80)
    print("DRIFT DETECTION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())