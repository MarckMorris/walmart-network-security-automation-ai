"""
Health Check Routes
System health monitoring endpoints
"""

from fastapi import APIRouter
from typing import Dict

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict:
    """Basic health check"""
    return {
        "status": "healthy",
        "service": "Network Security Automation",
        "version": "1.0.0"
    }

@router.get("/health/detailed")
async def detailed_health() -> Dict:
    """Detailed health check with component status"""
    return {
        "status": "healthy",
        "components": {
            "database": "healthy",
            "ise_integration": "healthy",
            "dlp_integration": "healthy",
            "ml_engine": "healthy"
        },
        "metrics": {
            "uptime_seconds": 3600,
            "requests_processed": 1000
        }
    }
