"""
Network Events Repository
Specialized queries for network events and time-series data
"""

from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from ..models.network_events import NetworkEvent
from .base_repository import BaseRepository


class EventRepository(BaseRepository[NetworkEvent]):
    """Repository for network events with time-series queries"""

    def __init__(self, session: Session):
        super().__init__(NetworkEvent, session)

    def get_events_by_time_range(
        self, start_time: datetime, end_time: datetime, limit: int = 1000
    ) -> List[NetworkEvent]:
        """Get events within a time range"""
        return (
            self.session.query(self.model)
            .filter(
                and_(
                    self.model.timestamp >= start_time, self.model.timestamp <= end_time
                )
            )
            .order_by(self.model.timestamp.desc())
            .limit(limit)
            .all()
        )

    def get_events_by_device(
        self, device_id: str, hours: int = 24
    ) -> List[NetworkEvent]:
        """Get recent events for a specific device"""
        start_time = datetime.utcnow() - timedelta(hours=hours)
        return (
            self.session.query(self.model)
            .filter(
                and_(
                    self.model.device_id == device_id,
                    self.model.timestamp >= start_time,
                )
            )
            .order_by(self.model.timestamp.desc())
            .all()
        )

    def get_events_by_source_ip(
        self, source_ip: str, hours: int = 24
    ) -> List[NetworkEvent]:
        """Get recent events from a source IP"""
        start_time = datetime.utcnow() - timedelta(hours=hours)
        return (
            self.session.query(self.model)
            .filter(
                and_(
                    self.model.source_ip == source_ip,
                    self.model.timestamp >= start_time,
                )
            )
            .order_by(self.model.timestamp.desc())
            .all()
        )

    def get_high_severity_events(
        self, hours: int = 24, limit: int = 100
    ) -> List[NetworkEvent]:
        """Get high severity events"""
        start_time = datetime.utcnow() - timedelta(hours=hours)
        return (
            self.session.query(self.model)
            .filter(
                and_(
                    self.model.severity.in_(["high", "critical"]),
                    self.model.timestamp >= start_time,
                )
            )
            .order_by(self.model.timestamp.desc())
            .limit(limit)
            .all()
        )

    def get_event_stats_by_type(self, hours: int = 24) -> dict:
        """Get event statistics grouped by type"""
        start_time = datetime.utcnow() - timedelta(hours=hours)

        stats = (
            self.session.query(
                self.model.event_type,
                func.count(self.model.id).label("count"),
                func.sum(self.model.bytes_sent).label("total_bytes_sent"),
                func.sum(self.model.bytes_received).label("total_bytes_received"),
            )
            .filter(self.model.timestamp >= start_time)
            .group_by(self.model.event_type)
            .all()
        )

        return {
            stat.event_type: {
                "count": stat.count,
                "total_bytes_sent": stat.total_bytes_sent or 0,
                "total_bytes_received": stat.total_bytes_received or 0,
            }
            for stat in stats
        }
