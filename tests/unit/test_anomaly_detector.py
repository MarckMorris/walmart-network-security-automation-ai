"""
Unit Tests for Anomaly Detector
Phase 7: ML model testing
"""

import pytest
import pandas as pd
import numpy as np
from src.ml.models.anomaly_detector import NetworkAnomalyDetector

class TestNetworkAnomalyDetector:
    """Test anomaly detection model"""
    
    def test_initialization(self):
        """Test model initialization"""
        detector = NetworkAnomalyDetector(contamination=0.1)
        assert detector.contamination == 0.1
        assert not detector.is_trained
    
    def test_feature_preparation(self, sample_network_event):
        """Test feature preparation"""
        detector = NetworkAnomalyDetector()
        df = pd.DataFrame([sample_network_event])
        features = detector.prepare_features(df)
        
        assert features.shape[0] == 1
        assert features.shape[1] == len(detector.feature_names)
    
    def test_training(self):
        """Test model training"""
        # Generate synthetic training data
        data = {
            'bytes_sent': np.random.randint(1000, 50000, 100),
            'bytes_received': np.random.randint(1000, 50000, 100),
            'packets_sent': np.random.randint(10, 100, 100),
            'packets_received': np.random.randint(10, 100, 100),
            'timestamp': pd.date_range('2024-01-01', periods=100, freq='H')
        }
        df = pd.DataFrame(data)
        
        detector = NetworkAnomalyDetector(contamination=0.1)
        metrics = detector.train(df)
        
        assert detector.is_trained
        assert metrics['samples_trained'] == 100
        assert 0 <= metrics['anomaly_rate'] <= 1
    
    def test_prediction(self):
        """Test anomaly prediction"""
        # Train model
        data = {
            'bytes_sent': np.random.randint(1000, 50000, 100),
            'bytes_received': np.random.randint(1000, 50000, 100),
            'packets_sent': np.random.randint(10, 100, 100),
            'packets_received': np.random.randint(10, 100, 100),
            'timestamp': pd.date_range('2024-01-01', periods=100, freq='H')
        }
        df = pd.DataFrame(data)
        
        detector = NetworkAnomalyDetector(contamination=0.1)
        detector.train(df)
        
        # Test prediction
        test_data = df.iloc[:10]
        predictions, scores = detector.predict(test_data)
        
        assert len(predictions) == 10
        assert len(scores) == 10
        assert all(p in [-1, 1] for p in predictions)
