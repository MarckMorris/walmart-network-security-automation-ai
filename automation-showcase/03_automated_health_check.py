import asyncio
from typing import Dict, List
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HealthCheckAutomation:
    """Automated health check system for ISE and DLP platforms"""

    async def check_ise_health(self) -> Dict:
        """Comprehensive ISE health check"""
        logger.info("Running ISE health check...")
        return {
            "service": "Cisco ISE",
            "timestamp": datetime.now().isoformat(),
            "checks": [
                {"name": "API Connectivity",    "status": "PASS", "message": "ISE API responding normally"},
                {"name": "Active Sessions",     "status": "PASS", "message": "15,234 sessions - within normal range"},
                {"name": "DB Replication",      "status": "PASS", "message": "All nodes synchronized"},
                {"name": "Certificate Expiry",  "status": "WARN", "message": "Certificate expires in 25 days"},
                {"name": "Disk Usage",          "status": "PASS", "message": "Disk usage at 72%"}
            ]
        }

    async def check_dlp_health(self) -> Dict:
        """Comprehensive DLP health check"""
        logger.info("Running DLP health check...")
        return {
            "service": "Symantec DLP",
            "timestamp": datetime.now().isoformat(),
            "checks": [
                {"name": "API Connectivity",    "status": "PASS", "message": "DLP API responding normally"},
                {"name": "Incident Queue",      "status": "PASS", "message": "42 incidents pending review"},
                {"name": "DLP Agents",          "status": "WARN", "message": "3 of 1,247 agents offline"},
                {"name": "Policy Distribution", "status": "PASS", "message": "All agents have latest policies"}
            ]
        }

    def generate_summary(self, reports: List[Dict]) -> Dict:
        """Generate overall health summary"""
        passed = warnings = failures = 0
        for report in reports:
            for check in report["checks"]:
                if check["status"] == "PASS":   passed += 1
                elif check["status"] == "WARN": warnings += 1
                elif check["status"] == "FAIL": failures += 1
        status = "CRITICAL" if failures > 0 else "DEGRADED" if warnings > 0 else "HEALTHY"
        return {
            "overall_status": status,
            "passed": passed,
            "warnings": warnings,
            "failures": failures,
            "timestamp": datetime.now().isoformat()
        }


async def main():
    print("=" * 80)
    print("AUTOMATED HEALTH CHECK SYSTEM - WALMART DEMO")
    print("=" * 80)
    print()

    health = HealthCheckAutomation()
    ise = await health.check_ise_health()
    dlp = await health.check_dlp_health()

    for report in [ise, dlp]:
        print(f"{report['service']} Health Report:")
        print("-" * 50)
        for check in report["checks"]:
            icon = "OK  " if check["status"] == "PASS" else "WARN" if check["status"] == "WARN" else "FAIL"
            print(f"  [{icon}] {check['name']}: {check['message']}")
        print()

    summary = health.generate_summary([ise, dlp])
    print("=" * 80)
    print(f"OVERALL STATUS: {summary['overall_status']}")
    print(f"Passed: {summary['passed']} | Warnings: {summary['warnings']} | Failures: {summary['failures']}")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())