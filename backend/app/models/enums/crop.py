import enum


class CropStatus(str, enum.Enum):
    optimal = "optimo"     
    mild_stress = "estres_leve"    
    severe_stress = "estres_severo"