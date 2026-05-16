from typing import Any

import pandas as pd

from backend.app.models.enums.crop import CropStatus
from backend.app.models.enums.humidity import AmbientHumidityAlertStatus
from backend.app.models.enums.temperature import LightTemperatureStatus, TemperatureAlertStatus
from backend.app.models.enums.watering import WateringStatus
from backend.app.schemas.predict_schema import PredictInput, PredictOutput

# Columnas en el orden exacto que espera el modelo entrenado
_FEATURES = ["temp", "hum_amb", "hum_suelo", "luz", "hora_dia"]
_OUTPUTS = ["alerta_temperatura", "alerta_luz", "alerta_humedad_ambiente", "riego", "estado_cultivo"]

_TEMP_MAP: dict[int, TemperatureAlertStatus] = {
    0: TemperatureAlertStatus.without_alert,
    1: TemperatureAlertStatus.mild_alert,
    2: TemperatureAlertStatus.alert,
}

_LIGHT_MAP: dict[int, LightTemperatureStatus] = {
    0: LightTemperatureStatus.enough_light,
    1: LightTemperatureStatus.little_light,
    2: LightTemperatureStatus.insufficient_light,
}

_HUMIDITY_MAP: dict[int, AmbientHumidityAlertStatus] = {
    0: AmbientHumidityAlertStatus.normal,
    1: AmbientHumidityAlertStatus.dry_air,
    2: AmbientHumidityAlertStatus.risk_of_mold,
}

_WATERING_MAP: dict[int, WateringStatus] = {
    0: WateringStatus.do_not_water,
    1: WateringStatus.watering,
}

_CROP_MAP: dict[str, CropStatus] = {
    "optimo": CropStatus.optimal,
    "estres_leve": CropStatus.mild_stress,
    "estres_severo": CropStatus.severe_stress,
}


def run_prediction(data: PredictInput, model_package: dict[str, Any]) -> PredictOutput:
    modelo = model_package["modelo"]
    le = model_package["encoder_estado"]

    # Mapeo schema (inglés) → columnas que espera el modelo (español)
    df = pd.DataFrame(
        [[data.temperature, data.environmental_humidity, data.soil_moisture, data.light, data.current_time_of_the_day]],
        columns=_FEATURES,
    )

    raw = dict(zip(_OUTPUTS, modelo.predict(df)[0]))
    estado_text: str = le.inverse_transform([int(raw["estado_cultivo"])])[0]

    return PredictOutput(
        temperature_alert=_TEMP_MAP[int(raw["alerta_temperatura"])],
        light_temperature=_LIGHT_MAP[int(raw["alerta_luz"])],
        ambient_humidity_alert=_HUMIDITY_MAP[int(raw["alerta_humedad_ambiente"])],
        watering=_WATERING_MAP[int(raw["riego"])],
        crop_status=_CROP_MAP[estado_text],
    )
