from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from uuid6 import uuid7

if TYPE_CHECKING:
    from backend.app.models.prediction_result import PredictionResult
from sqlalchemy import UUID, DateTime, Float, Integer, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base


class Predict(Base):
    __tablename__ = "predict"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    environmental_humidity: Mapped[float] = mapped_column(Float, nullable=False)
    soil_moisture: Mapped[float] = mapped_column(Float, nullable=False)
    light: Mapped[float] = mapped_column(Float, nullable=False)
    current_time_of_the_day: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="predictions")
    result: Mapped["PredictionResult"] = relationship("PredictionResult", back_populates="predict", uselist=False, cascade="all, delete-orphan")
