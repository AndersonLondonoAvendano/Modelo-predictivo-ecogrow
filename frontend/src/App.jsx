import { useState, useEffect } from 'react';
import { logout } from './api/client';
import { useTweaks } from './hooks/useTweaks';
import { applyPalette, applyDensity } from './utils/theme';
import { TWEAK_DEFAULTS } from './constants/tweakDefaults';
import LoginScreen from './components/LoginScreen';
import Sidebar from './components/Sidebar';
import BottomNav from './components/BottomNav';
import DashboardScreen from './components/DashboardScreen';
import PredictionScreen from './components/PredictionScreen';
import HistoryScreen from './components/HistoryScreen';

export default function App() {
  const [user, setUser] = useState(null);
  const [currentScreen, setCurrentScreen] = useState('dashboard');
  const [predictions, setPredictions] = useState([]);

  const tweaks = useTweaks(TWEAK_DEFAULTS);

  useEffect(() => {
    applyPalette(tweaks.palette, tweaks.darkMode);
    applyDensity(tweaks.density);
    document.body.classList.toggle('dark-mode', tweaks.darkMode);
  }, [tweaks.palette, tweaks.darkMode, tweaks.density]);

  useEffect(() => {
    applyPalette(TWEAK_DEFAULTS.palette, TWEAK_DEFAULTS.darkMode);
    applyDensity(TWEAK_DEFAULTS.density);
  }, []);

  const handleLogin = (userData) => setUser(userData);

  const handleLogout = async () => {
    if (confirm('¿Cerrar sesión?')) {
      try { await logout(); } catch (_) {}
      setUser(null);
      setCurrentScreen('dashboard');
      setPredictions([]);
    }
  };

  const handleAddPrediction = (prediction) =>
    setPredictions((prev) => [prediction, ...prev]);

  if (!user) return <LoginScreen onLogin={handleLogin} />;

  return (
    <div className="app-container">
      <Sidebar
        currentScreen={currentScreen}
        onNavigate={setCurrentScreen}
        user={user}
        onLogout={handleLogout}
      />

      {currentScreen === 'dashboard' && (
        <DashboardScreen
          predictions={predictions}
          onNavigate={setCurrentScreen}
          visualizationType={tweaks.alertVisualization}
        />
      )}

      {currentScreen === 'prediction' && (
        <PredictionScreen
          onAddPrediction={handleAddPrediction}
          onNavigate={setCurrentScreen}
        />
      )}

      {currentScreen === 'history' && (
        <HistoryScreen predictions={predictions} />
      )}

      <BottomNav currentScreen={currentScreen} onNavigate={setCurrentScreen} />
    </div>
  );
}
