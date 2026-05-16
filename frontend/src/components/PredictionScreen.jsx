import { useState } from 'react';
import { predict } from '../api/client';
import { getStatusColor, CROP_STATUS_MAP, WATERING_MAP, TEMP_ALERT_MAP, LIGHT_MAP, HUMIDITY_MAP } from '../utils/status';

export default function PredictionScreen({ onAddPrediction, onNavigate }) {
  const [formData, setFormData] = useState({ temperature: '', humidity: '', soilMoisture: '', light: '', hour: '' });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (field, value) => setFormData((prev) => ({ ...prev, [field]: value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setError(null);
    try {
      const data = await predict({
        temperature: parseFloat(formData.temperature),
        environmental_humidity: parseFloat(formData.humidity),
        soil_moisture: parseFloat(formData.soilMoisture),
        light: parseFloat(formData.light),
        current_time_of_the_day: parseInt(formData.hour),
      });

      const prediction = {
        id: Date.now(),
        timestamp: new Date().toLocaleString('es-MX', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }),
        cropStatus: CROP_STATUS_MAP[data.crop_status] || data.crop_status,
        temperature: parseFloat(formData.temperature),
        tempAlert: TEMP_ALERT_MAP[data.temperature_alert] || data.temperature_alert,
        lightAlert: LIGHT_MAP[data.light_temperature] || data.light_temperature,
        humidityAlert: HUMIDITY_MAP[data.ambient_humidity_alert] || data.ambient_humidity_alert,
        irrigationNeeded: WATERING_MAP[data.watering] || data.watering,
      };
      setResult(prediction);
      onAddPrediction(prediction);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="main-content">
      <div className="page-header">
        <h1 className="page-title">Nueva Predicción</h1>
        <p className="page-subtitle">Ingresa las lecturas de los sensores para obtener una predicción</p>
      </div>

      <div className="grid grid-2">
        <div className="card">
          <h3 className="card-title" style={{ marginBottom: 'calc(var(--space-6) * var(--density-multiplier))' }}>Datos del Sensor</h3>
          <form onSubmit={handleSubmit}>
            {[
              { field: 'temperature', label: 'Temperatura (°C)', placeholder: '24.5', hint: 'Rango típico: 15-35°C', step: '0.1', min: '-10', max: '60' },
              { field: 'humidity', label: 'Humedad Ambiental (%)', placeholder: '65', hint: 'Porcentaje de humedad relativa', step: '1', min: '0', max: '100' },
              { field: 'soilMoisture', label: 'Humedad de Suelo (0-1023)', placeholder: '512', hint: 'Lectura analógica del sensor', step: '1', min: '0', max: '1023' },
              { field: 'light', label: 'Luz (0-1023)', placeholder: '700', hint: 'Lectura del sensor de luz', step: '1', min: '0', max: '1023' },
              { field: 'hour', label: 'Hora del Día (0-23)', placeholder: '14', hint: 'Hora en formato 24h', step: '1', min: '0', max: '23' },
            ].map(({ field, label, placeholder, hint, step, min, max }) => (
              <div className="form-group" key={field}>
                <label className="form-label">{label}</label>
                <input
                  type="number"
                  step={step}
                  min={min}
                  max={max}
                  className="form-input"
                  placeholder={placeholder}
                  value={formData[field]}
                  onChange={(e) => handleChange(field, e.target.value)}
                  required
                />
                <div className="form-hint">{hint}</div>
              </div>
            ))}

            {error && (
              <div style={{ color: 'var(--palette-danger)', fontSize: '0.875rem', marginBottom: 'var(--space-4)', padding: 'var(--space-3)', background: 'var(--palette-danger-light)', borderRadius: 'var(--radius-md)' }}>
                {error}
              </div>
            )}

            <button type="submit" className="btn btn-primary btn-lg" style={{ width: '100%' }} disabled={loading}>
              {loading ? (
                <><span className="spinner" /> Analizando...</>
              ) : (
                <><span>🔮</span> Obtener Predicción</>
              )}
            </button>
          </form>
        </div>

        <div className="card">
          <h3 className="card-title" style={{ marginBottom: 'calc(var(--space-6) * var(--density-multiplier))' }}>Resultado de la Predicción</h3>

          {!result && !loading && (
            <div className="empty-state">
              <div className="empty-icon">📊</div>
              <div className="empty-title">Sin predicción</div>
              <div className="empty-description">Completa el formulario para obtener una predicción</div>
            </div>
          )}

          {loading && (
            <div className="empty-state">
              <div className="spinner" style={{ width: '48px', height: '48px', marginBottom: 'var(--space-4)' }} />
              <div className="empty-title">Procesando datos...</div>
            </div>
          )}

          {result && !loading && (
            <div>
              <div style={{ padding: 'calc(var(--space-6) * var(--density-multiplier))', background: `var(--palette-${getStatusColor(result.cropStatus)}-light)`, borderRadius: 'var(--radius-lg)', marginBottom: 'calc(var(--space-6) * var(--density-multiplier))', textAlign: 'center' }}>
                <div style={{ fontSize: 'calc(3rem * var(--density-multiplier))', marginBottom: 'calc(var(--space-3) * var(--density-multiplier))' }}>
                  {result.cropStatus.includes('Óptimo') ? '✅' : result.cropStatus.includes('leve') ? '⚠️' : '🚨'}
                </div>
                <div className="alert-label">Estado del Cultivo</div>
                <div style={{ fontSize: 'calc(2rem * var(--density-multiplier))', fontWeight: 700, color: `var(--palette-${getStatusColor(result.cropStatus)})`, marginTop: 'calc(var(--space-2) * var(--density-multiplier))' }}>
                  {result.cropStatus}
                </div>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: 'calc(var(--space-4) * var(--density-multiplier))' }}>
                {[
                  { label: 'Alerta de Temperatura', value: result.tempAlert },
                  { label: 'Alerta de Luz', value: result.lightAlert },
                  { label: 'Alerta de Humedad Ambiental', value: result.humidityAlert },
                  { label: 'Riego Necesario', value: result.irrigationNeeded },
                ].map(({ label, value }) => (
                  <div key={label}>
                    <div className="alert-label">{label}</div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span className="alert-value">{value}</span>
                      <span className={`badge badge-${getStatusColor(value)}`}>
                        <span className="badge-dot" />
                      </span>
                    </div>
                  </div>
                ))}
              </div>

              <button className="btn btn-secondary" style={{ width: '100%', marginTop: 'calc(var(--space-6) * var(--density-multiplier))' }} onClick={() => onNavigate('dashboard')}>
                Ver en Dashboard
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
