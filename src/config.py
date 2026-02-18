"""
Application Configuration
Centralized configuration management
"""

import logging
import os
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class DatabaseConfig:
    """Database configuration"""

    host: str
    port: int
    database: str
    username: str
    password: str
    pool_size: int = 10

    @property
    def connection_string(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class ISEConfig:
    """Cisco ISE configuration"""

    base_url: str
    username: str
    password: str
    verify_ssl: bool = True


@dataclass
class DLPConfig:
    """Symantec DLP configuration"""

    base_url: str
    username: str
    password: str
    verify_ssl: bool = True


@dataclass
class MLConfig:
    """ML models configuration"""

    models_dir: str
    training_data_dir: str
    inference_batch_size: int = 100
    anomaly_threshold: float = 0.1


class Config:
    """Main application configuration"""

    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

        # Database configuration
        self.database = DatabaseConfig(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            database=os.getenv("DB_NAME", "network_security_automation"),
            username=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
            pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
        )

        # Cisco ISE configuration
        self.ise = ISEConfig(
            base_url=os.getenv("ISE_URL", "http://localhost:9060"),
            username=os.getenv("ISE_USERNAME", "admin"),
            password=os.getenv("ISE_PASSWORD", "admin"),
            verify_ssl=os.getenv("ISE_VERIFY_SSL", "false").lower() == "true",
        )

        # Symantec DLP configuration
        self.dlp = DLPConfig(
            base_url=os.getenv("DLP_URL", "http://localhost:8080"),
            username=os.getenv("DLP_USERNAME", "admin"),
            password=os.getenv("DLP_PASSWORD", "admin"),
            verify_ssl=os.getenv("DLP_VERIFY_SSL", "false").lower() == "true",
        )

        # ML configuration
        self.ml = MLConfig(
            models_dir=os.getenv("ML_MODELS_DIR", "data/models"),
            training_data_dir=os.getenv("ML_TRAINING_DATA_DIR", "data/training"),
            inference_batch_size=int(os.getenv("ML_BATCH_SIZE", "100")),
            anomaly_threshold=float(os.getenv("ML_ANOMALY_THRESHOLD", "0.1")),
        )

        # API configuration
        self.api_host = os.getenv("API_HOST", "0.0.0.0")
        self.api_port = int(os.getenv("API_PORT", "8000"))

        logger.info(f"Configuration loaded for environment: {self.environment}")
