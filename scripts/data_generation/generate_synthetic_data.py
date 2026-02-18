"""
Synthetic Data Generator
Phase 4: Generate realistic network data for ML training
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class SyntheticDataGenerator:
    """Generate realistic synthetic network security data"""
    
    def __init__(self, seed: int = 42):
        np.random.seed(seed)
        random.seed(seed)
        self.ip_ranges = [
            "10.1.{}.{}",
            "192.168.{}.{}",
            "172.16.{}.{}"
        ]
        self.protocols = ['TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS', 'DNS', 'SSH']
        self.event_types = ['connection', 'auth', 'data_transfer', 'api_call', 'file_access']
        
    def generate_network_events(
        self, 
        num_events: int = 10000,
        anomaly_rate: float = 0.05,
        start_date: datetime = None
    ) -> pd.DataFrame:
        """Generate synthetic network events"""
        logger.info(f"Generating {num_events} synthetic network events...")
        
        if start_date is None:
            start_date = datetime.utcnow() - timedelta(days=30)
        
        events = []
        
        for i in range(num_events):
            # Random timestamp
            timestamp = start_date + timedelta(
                seconds=random.randint(0, 30 * 24 * 3600)
            )
            
            # Determine if this is an anomaly
            is_anomaly = random.random() < anomaly_rate
            
            # Generate IP addresses
            source_ip = self.ip_ranges[random.randint(0, 2)].format(
                random.randint(1, 254),
                random.randint(1, 254)
            )
            destination_ip = self.ip_ranges[random.randint(0, 2)].format(
                random.randint(1, 254),
                random.randint(1, 254)
            )
            
            # Generate traffic characteristics
            if is_anomaly:
                # Anomalous traffic patterns
                bytes_sent = random.randint(1000000, 10000000)  # Large transfer
                bytes_received = random.randint(100, 1000)  # Minimal response
                packets_sent = random.randint(500, 2000)
                severity = random.choice(['high', 'critical'])
            else:
                # Normal traffic patterns
                bytes_sent = random.randint(1000, 50000)
                bytes_received = random.randint(1000, 50000)
                packets_sent = random.randint(10, 100)
                severity = random.choice(['low', 'medium'])
            
            packets_received = packets_sent + random.randint(-10, 10)
            
            event = {
                'timestamp': timestamp,
                'source_ip': source_ip,
                'destination_ip': destination_ip,
                'source_port': random.randint(1024, 65535),
                'destination_port': random.choice([80, 443, 22, 3306, 5432, 8080]),
                'protocol': random.choice(self.protocols),
                'bytes_sent': bytes_sent,
                'bytes_received': bytes_received,
                'packets_sent': packets_sent,
                'packets_received': packets_received,
                'event_type': random.choice(self.event_types),
                'severity': severity,
                'device_id': f'device-{random.randint(1, 100):03d}',
                'location': random.choice(['store-001', 'store-002', 'hq-datacenter', 'cloud-az-east']),
                'is_anomaly': is_anomaly
            }
            
            events.append(event)
        
        df = pd.DataFrame(events)
        logger.info(f"Generated {len(df)} events ({df['is_anomaly'].sum()} anomalies)")
        
        return df
    
    def generate_timeseries_data(
        self,
        days: int = 90,
        interval_hours: int = 1
    ) -> pd.DataFrame:
        """Generate time-series data for capacity planning"""
        logger.info(f"Generating {days} days of time-series data...")
        
        start_date = datetime.utcnow() - timedelta(days=days)
        timestamps = pd.date_range(start=start_date, periods=days*24//interval_hours, freq=f'{interval_hours}H')
        
        # Base pattern with daily seasonality
        base_utilization = 50 + 20 * np.sin(np.linspace(0, days * 2 * np.pi, len(timestamps)))
        
        # Add hourly pattern
        hourly_pattern = 10 * np.sin(np.linspace(0, len(timestamps) * 2 * np.pi / 24, len(timestamps)))
        
        # Add random noise
        noise = np.random.normal(0, 5, len(timestamps))
        
        # Combine patterns
        bandwidth_utilization = np.clip(base_utilization + hourly_pattern + noise, 0, 100)
        
        df = pd.DataFrame({
            'timestamp': timestamps,
            'bandwidth_utilization': bandwidth_utilization,
            'device_id': 'core-router-01',
            'location': 'hq-datacenter'
        })
        
        logger.info(f"Generated {len(df)} time-series data points")
        
        return df
    
    def save_training_data(self, output_dir: str = "data/training") -> None:
        """Generate and save all training datasets"""
        from pathlib import Path
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate network events
        events_df = self.generate_network_events(num_events=50000)
        events_path = output_path / "network_events_training.csv"
        events_df.to_csv(events_path, index=False)
        logger.info(f"Saved network events to {events_path}")
        
        # Generate time-series data
        ts_df = self.generate_timeseries_data(days=90)
        ts_path = output_path / "timeseries_training.csv"
        ts_df.to_csv(ts_path, index=False)
        logger.info(f"Saved time-series data to {ts_path}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generator = SyntheticDataGenerator()
    generator.save_training_data()
