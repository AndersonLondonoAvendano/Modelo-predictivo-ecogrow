import enum


class AmbientHumidityAlertStatus(str, enum.Enum):
    normal = "normal"
    dry_air = "aire_seco"
    risk_of_mold = "riesgo_ongos"