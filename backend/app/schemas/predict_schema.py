from pydantic import BaseModel, Field

from backend.app.models.enums.crop import CropStatus
from backend.app.models.enums.humidity import AmbientHumidityAlertStatus
from backend.app.models.enums.temperature import LightTemperatureStatus, TemperatureAlertStatus
from backend.app.models.enums.watering import WateringStatus


class PredictInput(BaseModel):
    temperature: float = Field(..., ge=-10.0, le=60.0, description="Temperatura ambiental en °C")
    environmental_humidity: float = Field(..., ge=0.0, le=100.0, description="Humedad ambiental en %")
    soil_moisture: float = Field(..., ge=0.0, le=1023.0, description="Humedad del suelo (valor del sensor 0–1023)")
    light: float = Field(..., ge=0.0, le=1023.0, description="Intensidad lumínica (valor del sensor 0–1023)")
    current_time_of_the_day: int = Field(..., ge=0, le=23, description="Hora del día en formato 24 h (0–23)")


class PredictOutput(BaseModel):
    temperature_alert: TemperatureAlertStatus
    light_temperature: LightTemperatureStatus
    ambient_humidity_alert: AmbientHumidityAlertStatus
    watering: WateringStatus
    crop_status: CropStatus
