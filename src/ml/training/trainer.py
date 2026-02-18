"""
ML Model Trainer
Phase 4: Training pipeline for all ML models
"""

import logging
from typing import Dict, Optional
import pandas as pd
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)

class ModelTrainer:
    """Centralized ML model training orchestrator"""
    
    def __init__(self, data_dir: str = "data/training", models_dir: str = "data/models"):
        self.data_dir = Path(data_dir)
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
    def train_anomaly_detector(self, training_data_path: str) -> Dict:
        """Train isolation forest anomaly detector"""
        logger.info("Training anomaly detection model...")
        
        # Load training data
        df = pd.read_csv(training_data_path)
        
        # Import and train model - FIX: Import correcto
        from src.ml.models.anomaly_detector import NetworkAnomalyDetector
        
        detector = NetworkAnomalyDetector(contamination=0.1)
        metrics = detector.train(df)
        
        # Save model
        model_path = self.models_dir / "anomaly_detector_v1.joblib"
        detector.save_model(str(model_path))
        
        logger.info(f"Anomaly detector trained and saved to {model_path}")
        return metrics
    
    def train_lstm_predictor(self, training_data_path: str) -> Dict:
        """Train LSTM time-series predictor"""
        logger.info("Training LSTM prediction model...")
        
        try:
            # Load training data
            df = pd.read_csv(training_data_path, parse_dates=['timestamp'])
            df = df.set_index('timestamp')
            
            # Import and train model
            from src.ml.models.lstm_predictor import NetworkLSTMPredictor
            
            predictor = NetworkLSTMPredictor(sequence_length=24, forecast_horizon=6)
            metrics = predictor.train(df, target_column='bandwidth_utilization')
            
            # Save model
            model_path = self.models_dir / "lstm_predictor_v1"
            predictor.save_model(str(model_path))
            
            logger.info(f"LSTM predictor trained and saved to {model_path}")
            return metrics
        except Exception as e:
            logger.warning(f"LSTM training skipped (TensorFlow may not be installed): {e}")
            return {'status': 'skipped', 'reason': str(e)}
    
    def train_all_models(self) -> Dict:
        """Train all ML models"""
        results = {}
        
        try:
            # Train anomaly detector
            anomaly_data = self.data_dir / "network_events_training.csv"
            if anomaly_data.exists():
                results['anomaly_detector'] = self.train_anomaly_detector(str(anomaly_data))
            
            # Train LSTM predictor
            lstm_data = self.data_dir / "timeseries_training.csv"
            if lstm_data.exists():
                results['lstm_predictor'] = self.train_lstm_predictor(str(lstm_data))
            
            logger.info("All models trained successfully")
            
        except Exception as e:
            logger.error(f"Error training models: {e}", exc_info=True)
        
        return results
