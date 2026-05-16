import { COLOR_PALETTES } from '../constants/palettes';

export function applyPalette(paletteName, isDark) {
  const palette = COLOR_PALETTES[paletteName];
  if (!palette) return;
  const colors = isDark ? { ...palette.colors, ...palette.darkColors } : palette.colors;
  const root = document.documentElement;
  root.style.setProperty('--palette-bg', colors.bg);
  root.style.setProperty('--palette-surface', colors.surface);
  root.style.setProperty('--palette-border', colors.border);
  root.style.setProperty('--palette-text-primary', colors.textPrimary);
  root.style.setProperty('--palette-text-secondary', colors.textSecondary);
  root.style.setProperty('--palette-text-tertiary', colors.textTertiary);
  root.style.setProperty('--palette-primary', colors.primary);
  root.style.setProperty('--palette-primary-hover', colors.primaryHover);
  root.style.setProperty('--palette-primary-light', colors.primaryLight);
  if (colors.success) root.style.setProperty('--palette-success', colors.success);
  root.style.setProperty('--palette-success-light', colors.successLight);
  if (colors.warning) root.style.setProperty('--palette-warning', colors.warning);
  root.style.setProperty('--palette-warning-light', colors.warningLight);
  if (colors.danger) root.style.setProperty('--palette-danger', colors.danger);
  root.style.setProperty('--palette-danger-light', colors.dangerLight);
}

export function applyDensity(density) {
  const densityMap = { compact: 0.85, default: 1, comfortable: 1.2 };
  document.documentElement.style.setProperty(
    '--density-multiplier',
    String(densityMap[density] ?? 1)
  );
}
