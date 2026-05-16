export function getStatusColor(status) {
  if (
    status.includes('Óptimo') ||
    status.includes('Sin alerta') ||
    status.includes('suficiente') ||
    status.includes('Normal') ||
    status === 'No'
  ) return 'success';

  if (
    status.includes('leve') ||
    status.includes('Poca') ||
    status.includes('seco')
  ) return 'warning';

  return 'danger';
}

export const CROP_STATUS_MAP = {
  optimo: 'Óptimo',
  estres_leve: 'Estrés leve',
  estres_severo: 'Estrés severo',
};

export const WATERING_MAP = {
  regar: 'Sí',
  no_regar: 'No',
};

export const TEMP_ALERT_MAP = {
  sin_alerta: 'Sin alerta',
  alerta_leve: 'Alerta leve',
  alerta: 'Alerta severa',
};

export const LIGHT_MAP = {
  luz_suficiente: 'Luz suficiente',
  poca_luz: 'Poca luz',
  luz_insuficiente: 'Luz insuficiente',
};

export const HUMIDITY_MAP = {
  normal: 'Normal',
  aire_seco: 'Aire seco',
  riesgo_ongos: 'Riesgo de hongos',
};
