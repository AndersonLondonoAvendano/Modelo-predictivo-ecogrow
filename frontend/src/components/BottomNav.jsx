export default function BottomNav({ currentScreen, onNavigate }) {
  return (
    <nav className="bottom-nav">
      <div className="bottom-nav-items">
        <button
          className={`bottom-nav-item ${currentScreen === 'dashboard' ? 'active' : ''}`}
          onClick={() => onNavigate('dashboard')}
        >
          <span className="bottom-nav-icon">📊</span>
          <span>Dashboard</span>
        </button>

        <button
          className={`bottom-nav-item ${currentScreen === 'prediction' ? 'active' : ''}`}
          onClick={() => onNavigate('prediction')}
        >
          <span className="bottom-nav-icon">🔮</span>
          <span>Predicción</span>
        </button>

        <button
          className={`bottom-nav-item ${currentScreen === 'history' ? 'active' : ''}`}
          onClick={() => onNavigate('history')}
        >
          <span className="bottom-nav-icon">📜</span>
          <span>Historial</span>
        </button>
      </div>
    </nav>
  );
}
