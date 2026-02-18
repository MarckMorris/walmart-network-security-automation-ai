"""
Pytest Configuration and Fixtures
Phase 7: Test infrastructure
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

@pytest.fixture
def sample_network_event():
    """Sample network event for testing"""
    return {
        'timestamp': '2024-01-01T00:00:00',
        'source_ip': '10.1.1.100',
        'destination_ip': '10.1.2.200',
        'source_port': 52000,
        'destination_port': 443,
        'protocol': 'TCP',
        'bytes_sent': 1500,
        'bytes_received': 2000,
        'packets_sent': 10,
        'packets_received': 12,
        'event_type': 'connection',
        'severity': 'low',
        'device_id': 'device-001',
        'location': 'store-001'
    }

@pytest.fixture
def sample_security_incident():
    """Sample security incident for testing"""
    return {
        'type': 'data_exfiltration',
        'severity': 'high',
        'confidence': 0.85,
        'mac_address': '00:11:22:33:44:55',
        'source_ip': '10.1.1.100'
    }
