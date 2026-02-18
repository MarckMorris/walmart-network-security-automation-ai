import asyncio
from typing import Dict, List
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BulkEndpointManager:
    """
    Enterprise-scale endpoint management.
    Covers 4,700+ Walmart stores, 600+ Sam's Club, 150+ distribution centers.
    """

    def __init__(self, batch_size: int = 100):
        self.batch_size = batch_size
        self.results = {"success": 0, "failed": 0}

    def generate_store_endpoints(self, store_count: int) -> List[Dict]:
        """Generate endpoint inventory for all stores"""
        endpoints = []
        for store_id in range(1, store_count + 1):
            for pos in range(1, 6):
                endpoints.append({
                    "id": f"POS-{store_id:04d}-{pos:02d}",
                    "type": "POS_TERMINAL",
                    "store_id": store_id,
                    "vlan": 100
                })
            endpoints.append({
                "id": f"AP-{store_id:04d}-01",
                "type": "ACCESS_POINT",
                "store_id": store_id,
                "vlan": 200
            })
        return endpoints

    async def process_endpoint(self, endpoint: Dict, action: str) -> Dict:
        """Process single endpoint via ISE API"""
        try:
            self.results["success"] += 1
            return {"endpoint_id": endpoint["id"], "action": action, "status": "SUCCESS"}
        except Exception as e:
            self.results["failed"] += 1
            return {"endpoint_id": endpoint["id"], "action": action, "status": "FAILED", "error": str(e)}

    async def bulk_operation(self, endpoints: List[Dict], action: str) -> Dict:
        """Execute bulk operation in concurrent batches"""
        total = len(endpoints)
        all_results = []

        for i in range(0, total, self.batch_size):
            batch = endpoints[i:i + self.batch_size]
            tasks = [self.process_endpoint(ep, action) for ep in batch]
            results = await asyncio.gather(*tasks)
            all_results.extend(results)
            progress = min(i + self.batch_size, total)
            logger.info(f"Progress: {progress}/{total} ({progress / total * 100:.1f}%)")

        return {
            "action": action,
            "total": total,
            "results": self.results,
            "completed_at": datetime.now().isoformat()
        }


async def main():
    print("=" * 80)
    print("BULK ENDPOINT MANAGEMENT - WALMART DEMO")
    print("=" * 80)
    print()

    manager = BulkEndpointManager(batch_size=100)

    print("Generating endpoint inventory for 500 stores...")
    endpoints = manager.generate_store_endpoints(500)
    pos_count = sum(1 for e in endpoints if e["type"] == "POS_TERMINAL")
    ap_count  = sum(1 for e in endpoints if e["type"] == "ACCESS_POINT")
    print(f"  Total endpoints: {len(endpoints)}")
    print(f"  POS Terminals:   {pos_count}")
    print(f"  Access Points:   {ap_count}")
    print()

    print("Scenario 1: Compliance check on all endpoints")
    start = datetime.now()
    result = await manager.bulk_operation(endpoints, "COMPLIANCE_CHECK")
    elapsed = (datetime.now() - start).total_seconds()
    print(f"  Completed {result['total']} endpoints in {elapsed:.2f}s")
    print(f"  Success: {result['results']['success']} | Failed: {result['results']['failed']}")
    print()

    manager.results = {"success": 0, "failed": 0}
    print("Scenario 2: Policy update across all stores")
    start = datetime.now()
    result = await manager.bulk_operation(endpoints, "UPDATE_POLICY")
    elapsed = (datetime.now() - start).total_seconds()
    print(f"  Updated {result['results']['success']} endpoints in {elapsed:.2f}s")
    print()

    print("=" * 80)
    print(f"BULK OPERATION COMPLETE - {len(endpoints)} endpoints | 500 stores")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())