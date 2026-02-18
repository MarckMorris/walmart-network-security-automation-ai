"""
ML Predictions Model
Stores ML model predictions and performance metrics
"""

import uuid

from sqlalchemy import Column, DateTime, Float, Index, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID

from .base import Base, TimestampMixin


class MLPrediction(Base, TimestampMixin):
    """ML model prediction results"""

    __tablename__ = "ml_predictions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_name = Column(String(100), nullable=False, index=True)
    model_version = Column(String(50), nullable=False)
    prediction_type = Column(String(50), nullable=False)
    input_features = Column(JSONB)
    prediction_result = Column(JSONB)
    confidence_score = Column(Float)
    inference_time_ms = Column(Float)
    prediction_timestamp = Column(DateTime, nullable=False, index=True)
    actual_outcome = Column(JSONB)
    was_correct = Column(Integer)

    __table_args__ = (
        Index(
            "idx_ml_predictions_model_timestamp", "model_name", "prediction_timestamp"
        ),
    )
