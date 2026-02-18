from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .routes import health, anomaly
from .metrics import get_metrics

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Network Security Automation API",
    description="AI-Driven Network Security Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(anomaly.router, prefix="/api/v1", tags=["anomaly"])

# Metrics endpoint
@app.get("/metrics")
async def metrics():
    return get_metrics()

@app.on_event("startup")
async def startup_event():
    logger.info("API starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("API shutting down...")
