import { useState } from 'react';
import { login } from '../api/client';

export default function LoginScreen({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const data = await login(email, password);
      onLogin({ name: data.user.email.split('@')[0], email: data.user.email });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <div className="login-logo">🌱</div>
          <h1 className="login-title">EcoGrow</h1>
          <p className="login-subtitle">Monitoreo inteligente de cultivos</p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Correo electrónico</label>
            <input
              type="email"
              className="form-input"
              placeholder="tu@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Contraseña</label>
            <input
              type="password"
              className="form-input"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && (
            <div style={{
              color: 'var(--palette-danger)',
              fontSize: '0.875rem',
              marginBottom: 'var(--space-4)',
              padding: 'var(--space-3)',
              background: 'var(--palette-danger-light)',
              borderRadius: 'var(--radius-md)',
            }}>
              {error}
            </div>
          )}

          <button
            type="submit"
            className="btn btn-primary btn-lg"
            style={{ width: '100%' }}
            disabled={loading}
          >
            {loading ? <span className="spinner" /> : 'Iniciar sesión'}
          </button>
        </form>
      </div>
    </div>
  );
}
