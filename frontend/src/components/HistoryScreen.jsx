import { getStatusColor } from '../utils/status';

export default function HistoryScreen({ predictions }) {
  if (predictions.length === 0) {
    return (
      <div className="main-content">
        <div className="page-header">
          <h1 className="page-title">Historial</h1>
          <p className="page-subtitle">Registro de predicciones anteriores</p>
        </div>
        <div className="card">
          <div className="empty-state">
            <div className="empty-icon">📜</div>
            <div className="empty-title">Sin historial</div>
            <div className="empty-description">Las predicciones que realices aparecerán aquí</div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="main-content">
      <div className="page-header">
        <h1 className="page-title">Historial</h1>
        <p className="page-subtitle">
          {predictions.length} predicción{predictions.length !== 1 ? 'es' : ''} registrada{predictions.length !== 1 ? 's' : ''}
        </p>
      </div>

      <div className="table-container">
        <table className="table">
          <thead>
            <tr>
              <th>Fecha y Hora</th>
              <th>Estado del Cultivo</th>
              <th>Temperatura</th>
              <th>Alerta Temp.</th>
              <th>Alerta Luz</th>
              <th>Alerta Humedad</th>
              <th>Riego</th>
            </tr>
          </thead>
          <tbody>
            {predictions.map((pred) => (
              <tr key={pred.id}>
                <td style={{ fontFamily: 'var(--font-mono)', fontSize: 'calc(0.8125rem * var(--density-multiplier))' }}>{pred.timestamp}</td>
                <td><span className={`badge badge-${getStatusColor(pred.cropStatus)}`}>{pred.cropStatus}</span></td>
                <td style={{ fontWeight: 600 }}>{pred.temperature}°C</td>
                <td><span className={`badge badge-${getStatusColor(pred.tempAlert)}`}><span className="badge-dot" />{pred.tempAlert}</span></td>
                <td><span className={`badge badge-${getStatusColor(pred.lightAlert)}`}><span className="badge-dot" />{pred.lightAlert}</span></td>
                <td><span className={`badge badge-${getStatusColor(pred.humidityAlert)}`}><span className="badge-dot" />{pred.humidityAlert}</span></td>
                <td><span className={`badge badge-${getStatusColor(pred.irrigationNeeded)}`}>{pred.irrigationNeeded}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
