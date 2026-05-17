import { getStatusColor } from '../utils/status';

function AlertCardView({ label, value, icon }) {
  const status = getStatusColor(value);
  return (
    <div className="alert-card">
      <div className="alert-icon" style={{ background: `var(--palette-${status}-light)`, color: `var(--palette-${status})` }}>
        {icon}
      </div>
      <div className="alert-content">
        <div className="alert-label">{label}</div>
        <div className="alert-value">{value}</div>
      </div>
      <span className={`badge badge-${status}`}>
        <span className="badge-dot" />
      </span>
    </div>
  );
}

function StatCardView({ label, value, icon }) {
  const status = getStatusColor(value);
  return (
    <div className="stat-card">
      <div className="stat-icon" style={{ background: `var(--palette-${status}-light)`, color: `var(--palette-${status})` }}>
        {icon}
      </div>
      <div className="stat-label">{label}</div>
      <div className="stat-value">{value}</div>
    </div>
  );
}

function GaugeView({ label, value, icon }) {
  const status = getStatusColor(value);
  const percentage = status === 'success' ? 85 : status === 'warning' ? 50 : 25;
  return (
    <div className="card">
      <div className="alert-label" style={{ textAlign: 'center', marginBottom: '1rem' }}>{label}</div>
      <div className="gauge-container">
        <svg viewBox="0 0 200 120" className="gauge">
          <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="var(--palette-border)" strokeWidth="16" strokeLinecap="round" />
          <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke={`var(--palette-${status})`} strokeWidth="16" strokeLinecap="round" strokeDasharray={`${percentage * 2.51} 251`} />
          <text x="100" y="80" textAnchor="middle" fontSize="32">{icon}</text>
        </svg>
      </div>
      <div className="alert-value" style={{ textAlign: 'center', marginTop: '1rem' }}>{value}</div>
    </div>
  );
}

export default function DashboardScreen({ predictions, onNavigate, visualizationType }) {
  const latest = predictions[0] || null;

  const AlertComponent =
    visualizationType === 'cards' ? AlertCardView :
    visualizationType === 'stats' ? StatCardView :
    GaugeView;

  if (!latest) {
    return (
      <div className="main-content">
        <div className="page-header">
          <h1 className="page-title">Dashboard</h1>
          <p className="page-subtitle">Estado actual de tu cultivo</p>
        </div>
        <div className="card">
          <div className="empty-state">
            <div className="empty-icon">🌱</div>
            <div className="empty-title">Sin datos disponibles</div>
            <div className="empty-description">Realiza tu primera predicción para ver el estado de tu cultivo</div>
            <button className="btn btn-primary" style={{ marginTop: 'var(--space-6)' }} onClick={() => onNavigate('prediction')}>
              Nueva Predicción
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="main-content">
      <div className="page-header">
        <h1 className="page-title">Dashboard</h1>
        <p className="page-subtitle">Estado actual de tu cultivo · Última actualización: {latest.timestamp}</p>
      </div>

      <div className="card" style={{ marginBottom: 'calc(var(--space-6) * var(--density-multiplier))' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 'var(--space-6)', flexWrap: 'wrap' }}>
          <div style={{ flex: 1 }}>
            <div className="alert-label">Estado del Cultivo</div>
            <h2 style={{ fontSize: 'calc(2.5rem * var(--density-multiplier))', fontWeight: 700, marginTop: 'calc(var(--space-2) * var(--density-multiplier))', marginBottom: 'calc(var(--space-3) * var(--density-multiplier))', color: `var(--palette-${getStatusColor(latest.cropStatus)})` }}>
              {latest.cropStatus}
            </h2>
            <div style={{ display: 'flex', gap: 'var(--space-4)', flexWrap: 'wrap' }}>
              <div>
                <span style={{ fontSize: 'calc(0.875rem * var(--density-multiplier))', color: 'var(--palette-text-tertiary)' }}>Temperatura</span>
                <div style={{ fontSize: 'calc(1.5rem * var(--density-multiplier))', fontWeight: 700 }}>{latest.temperature}°C</div>
              </div>
              <div>
                <span style={{ fontSize: 'calc(0.875rem * var(--density-multiplier))', color: 'var(--palette-text-tertiary)' }}>Riego</span>
                <div style={{ fontSize: 'calc(1.5rem * var(--density-multiplier))', fontWeight: 700 }}>{latest.irrigationNeeded}</div>
              </div>
            </div>
          </div>
          <button className="btn btn-primary btn-lg" onClick={() => onNavigate('prediction')}>
            <span>🔮</span>
            Nueva Predicción
          </button>
        </div>
      </div>

      <div className="grid grid-4">
        <AlertComponent label="Alerta de Temperatura" value={latest.tempAlert} icon="🌡️" />
        <AlertComponent label="Intensidad de Luz" value={latest.lightAlert} icon="☀️" />
        <AlertComponent label="Alerta de Humedad Ambiental" value={latest.humidityAlert} icon="💧" />
        <AlertComponent label="Riego Necesario" value={latest.irrigationNeeded} icon="🚿" />
      </div>
    </div>
  );
}
