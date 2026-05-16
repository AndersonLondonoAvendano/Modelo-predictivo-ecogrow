from __future__ import annotations

import uuid
from typing import TYPE_CHECKING
from uuid6 import uuid7
from sqlalchemy import Enum as SAEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

if TYPE_CHECKING:
    from backend.app.models.predict import Predict

from backend.app.models.base import Base
from backend.app.models.enums.crop import CropStatus
from backend.app.models.enums.temperature import TemperatureAlertStatus, LightTemperatureStatus
from backend.app.models.enums.humidity import AmbientHumidityAlertStatus
from backend.app.models.enums.watering import WateringStatus


class PredictionResult(Base):
    __tablename__ = "prediction_results"


    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    predict_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("predict.id", ondelete="CASCADE"), nullable=False, index=True)

    temperature_alert: Mapped[TemperatureAlertStatus] = mapped_column(SAEnum(TemperatureAlertStatus, name="temperature_status"), nullable=False, default=TemperatureAlertStatus.without_alert)

    light_temperature: Mapped[LightTemperatureStatus] = mapped_column(SAEnum(LightTemperatureStatus, name="light_temperature_status"), nullable=False, default=LightTemperatureStatus.enough_light)

    ambient_humidity_alert: Mapped[AmbientHumidityAlertStatus] = mapped_column(SAEnum(AmbientHumidityAlertStatus, name="ambient_status"), nullable=False, default=AmbientHumidityAlertStatus.normal)

    watering: Mapped[WateringStatus] = mapped_column(SAEnum(WateringStatus, name="watering_status"), nullable=False, default=WateringStatus.do_not_water)
    
    crop_status: Mapped[CropStatus] = mapped_column(SAEnum(CropStatus, name="crop_status"), nullable=False, default=CropStatus.optimal)

    predict: Mapped["Predict"] = relationship("Predict", back_populates="result")