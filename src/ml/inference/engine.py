"""
ML Inference Engine
Phase 4: Real-time inference for trained models
"""

import logging
import time
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

logger = logging.getLogger(__name__)


class InferenceEngine:
    """ML inference engine for real-time predictions"""

    def __init__(self, models_dir: str = "data/models"):
        self.models_dir = Path(models_dir)
        self.anomaly_detector = None
        self.lstm_predictor = None
        self.load_models()

    def load_models(self) -> None:
        """Load all trained models"""
        try:
            # Load anomaly detector - FIX: Import correcto
            from src.ml.models.anomaly_detector import NetworkAnomalyDetector

            anomaly_path = self.models_dir / "anomaly_detector_v1.joblib"
            if anomaly_path.exists():
                self.anomaly_detector = NetworkAnomalyDetector.load_model(
                    str(anomaly_path)
                )
                logger.info("Anomaly detector loaded")
            else:
                logger.warning(f"Anomaly detector model not found at {anomaly_path}")

            # Load LSTM predictor
            from src.ml.models.lstm_predictor import NetworkLSTMPredictor

            lstm_path = self.models_dir / "lstm_predictor_v1"
            if (lstm_path.parent / f"{lstm_path.name}.h5").exists():
                self.lstm_predictor = NetworkLSTMPredictor.load_model(str(lstm_path))
                logger.info("LSTM predictor loaded")
            else:
                logger.warning(f"LSTM predictor model not found at {lstm_path}")

        except Exception as e:
            logger.error(f"Error loading models: {e}", exc_info=True)

    def detect_anomalies(self, events_df: pd.DataFrame) -> pd.DataFrame:
        """Detect anomalies in network events"""
        if self.anomaly_detector is None:
            logger.warning("Anomaly detector not loaded")
            return events_df

        start_time = time.time()
        results = self.anomaly_detector.detect_anomalies(events_df)
        inference_time = (time.time() - start_time) * 1000  # Convert to ms

        logger.info(f"Anomaly detection completed in {inference_time:.2f}ms")

        return results

    def forecast_capacity(
        self, historical_df: pd.DataFrame, steps: int = 6
    ) -> pd.DataFrame:
        """Forecast future capacity needs"""
        if self.lstm_predictor is None:
            logger.warning("LSTM predictor not loaded")
            return pd.DataFrame()

        start_time = time.time()
        forecast = self.lstm_predictor.forecast(
            historical_df, feature_columns=["bandwidth_utilization"], steps_ahead=steps
        )
        inference_time = (time.time() - start_time) * 1000

        logger.info(f"Capacity forecast completed in {inference_time:.2f}ms")

        return forecast
