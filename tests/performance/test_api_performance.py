"""
Performance Tests
Phase 7: Load and performance testing
"""

import pytest
import time
import pandas as pd
import numpy as np
from src.ml.models.anomaly_detector import NetworkAnomalyDetector

@pytest.mark.performance
class TestPerformance:
    """Performance benchmarks"""
    
    def test_anomaly_detection_latency(self):
        """Test anomaly detection latency < 100ms for 100 events"""
        # Generate test data
        data = {
            'bytes_sent': np.random.randint(1000, 50000, 1000),
            'bytes_received': np.random.randint(1000, 50000, 1000),
            'packets_sent': np.random.randint(10, 100, 1000),
            'packets_received': np.random.randint(10, 100, 1000),
            'timestamp': pd.date_range('2024-01-01', periods=1000, freq='H')
        }
        df = pd.DataFrame(data)
        
        # Train model
        detector = NetworkAnomalyDetector()
        detector.train(df[:800])
        
        # Test inference latency
        test_data = df[800:][:100]
        
        start = time.time()
        results = detector.detect_anomalies(test_data)
        latency = (time.time() - start) * 1000  # Convert to ms
        
        assert latency < 100, f"Latency {latency}ms exceeds 100ms threshold"
