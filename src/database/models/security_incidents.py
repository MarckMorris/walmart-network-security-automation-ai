"""
Security Incidents Model
Stores detected security incidents and remediation actions
"""

from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import uuid
import enum

class IncidentStatus(enum.Enum):
    """Incident status enum"""
    DETECTED = "detected"
    ANALYZING = "analyzing"
    REMEDIATING = "remediating"
    RESOLVED = "resolved"
    ESCALATED = "escalated"

class IncidentSeverity(enum.Enum):
    """Incident severity enum"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class SecurityIncident(Base, TimestampMixin):
    """Security incident model"""
    __tablename__ = 'security_incidents'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_type = Column(String(100), nullable=False)
    status = Column(SQLEnum(IncidentStatus), nullable=False, default=IncidentStatus.DETECTED)
    severity = Column(SQLEnum(IncidentSeverity), nullable=False)
    confidence_score = Column(Float, nullable=False)
    source_system = Column(String(50), nullable=False)
    affected_assets = Column(JSONB)
    detection_method = Column(String(100))
    ai_reasoning = Column(JSONB)
    remediation_actions = Column(JSONB)
    human_review_required = Column(Integer, default=0)
    resolved_at = Column(DateTime)
    resolved_by = Column(String(100))
    notes = Column(String)
