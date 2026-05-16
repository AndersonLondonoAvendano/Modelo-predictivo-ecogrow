import enum


class TemperatureAlertStatus(str, enum.Enum):
    without_alert = "sin_alerta"
    mild_alert = "alerta_leve"
    alert = "alerta"


class LightTemperatureStatus(str, enum.Enum):
    enough_light = "luz_suficiente"
    little_light = "poca_luz"
    insufficient_light = "luz_insuficiente"