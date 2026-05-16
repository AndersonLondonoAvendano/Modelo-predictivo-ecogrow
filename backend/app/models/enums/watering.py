import enum


class WateringStatus(str, enum.Enum):
    do_not_water = "no_regar"
    watering = "regar"