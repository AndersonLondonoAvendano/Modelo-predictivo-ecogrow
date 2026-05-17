export default function Sidebar({ currentScreen, onNavigate, user, onLogout }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="logo">
          <div className="logo-icon">🌱</div>
          <span>EcoGrow</span>
        </div>
      </div>

      <nav className="nav">
        <button
          className={`nav-item ${currentScreen === 'dashboard' ? 'active' : ''}`}
          onClick={() => onNavigate('dashboard')}
        >
          <span className="nav-icon">📊</span>
          <span>Dashboard</span>
        </button>

        <button
          className={`nav-item ${currentScreen === 'prediction' ? 'active' : ''}`}
          onClick={() => onNavigate('prediction')}
        >
          <span className="nav-icon">🔮</span>
          <span>Nueva Predicción</span>
        </button>

        <button
          className={`nav-item ${currentScreen === 'history' ? 'active' : ''}`}
          onClick={() => onNavigate('history')}
        >
          <span className="nav-icon">📜</span>
          <span>Historial</span>
        </button>
      </nav>

      <div className="sidebar-footer">
        <div className="user-info" onClick={onLogout} title="Cerrar sesión">
          <div className="user-avatar">{user.name.charAt(0).toUpperCase()}</div>
          <div className="user-details">
            <div className="user-name">{user.name}</div>
            <div className="user-email">{user.email}</div>
          </div>
        </div>
      </div>
    </aside>
  );
}
