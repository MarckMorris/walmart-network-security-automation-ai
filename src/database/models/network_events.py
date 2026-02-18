"""
Network Events Model
Stores network telemetry and events for analysis
"""

import uuid

from sqlalchemy import JSON, Column, DateTime, Float, Index, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID

from .base import Base, TimestampMixin


class NetworkEvent(Base, TimestampMixin):
    """Network event model for time-series data"""

    __tablename__ = "network_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, nullable=False, index=True)
    source_ip = Column(String(45), nullable=False, index=True)
    destination_ip = Column(String(45), nullable=False)
    source_port = Column(Integer)
    destination_port = Column(Integer)
    protocol = Column(String(10), nullable=False)
    bytes_sent = Column(Integer)
    bytes_received = Column(Integer)
    packets_sent = Column(Integer)
    packets_received = Column(Integer)
    event_type = Column(String(50), nullable=False, index=True)
    severity = Column(String(20), nullable=False)
    device_id = Column(String(100), index=True)
    location = Column(String(100), index=True)
    event_metadata = Column(JSONB)  # CAMBIADO: metadata -> event_metadata

    # Indexes for time-series queries
    __table_args__ = (
        Index("idx_network_events_timestamp_device", "timestamp", "device_id"),
        Index("idx_network_events_source_ip_timestamp", "source_ip", "timestamp"),
    )
