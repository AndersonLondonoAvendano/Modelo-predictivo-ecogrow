import os
import sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')
import matplotlib.pyplot as plt
import seaborn as sns


RUTA_DATASET = os.path.join(os.path.dirname(__file__), '..', 'data', 'dataset_ecogrow_v2.csv')
RUTA_DOCS = os.path.join(os.path.dirname(__file__), '..', 'docs')

COLUMNAS_ENTRADA = ['temp', 'hum_amb', 'hum_suelo', 'luz', 'hora_dia']
COLUMNAS_SALIDA  = ['alerta_temperatura', 'alerta_luz', 'alerta_humedad_ambiente',
                    'riego', 'estado_cultivo']


def cargar_dataset(ruta: str) -> pd.DataFrame:
    """Carga el CSV y devuelve un DataFrame."""
    try:
        df = pd.read_csv(ruta)
        print(f"Dataset cargado desde: {ruta}")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")


def analizar_forma(df: pd.DataFrame) -> None:
    """Imprime la forma (filas × columnas) del dataframe."""
    print("\n── FORMA DEL DATAFRAME ──────────────────────────────")
    print(f"  Filas: {df.shape[0]}  |  Columnas: {df.shape[1]}")


def analizar_nulos(df: pd.DataFrame) -> None:
    """Imprime los valores nulos por columna."""
    print("\n── VALORES NULOS POR COLUMNA ────────────────────────")
    nulos = df.isnull().sum()
    for col, n in nulos.items():
        estado = "✓ sin nulos" if n == 0 else f"⚠ {n} nulo(s)"
        print(f"  {col:<30} {estado}")


def distribucion_salidas(df: pd.DataFrame) -> None:
    """Imprime value_counts de cada columna de salida."""
    print("\n── DISTRIBUCIÓN DE COLUMNAS DE SALIDA ───────────────")
    for col in COLUMNAS_SALIDA:
        print(f"\n  {col}:")
        conteo = df[col].value_counts().sort_index()
        for valor, cnt in conteo.items():
            pct = cnt / len(df) * 100
            print(f"    {str(valor):<20}  {cnt:>4} filas  ({pct:.1f}%)")


def estadisticas_entradas(df: pd.DataFrame) -> None:
    """Imprime describe() de las columnas de entrada."""
    print("\n── ESTADÍSTICAS DESCRIPTIVAS DE ENTRADAS ────────────")
    print(df[COLUMNAS_ENTRADA].describe().to_string())


def correlacion_con_riego(df: pd.DataFrame) -> None:
    """Imprime la correlación de cada entrada con la variable 'riego'."""
    print("\n── CORRELACIÓN DE ENTRADAS CON 'riego' ──────────────")
    correlaciones = (
        df[COLUMNAS_ENTRADA + ['riego']]
        .corr()['riego']
        .drop('riego')
        .sort_values(key=abs, ascending=False)
    )
    for variable, valor in correlaciones.items():
        barra = '█' * int(abs(valor) * 20)
        signo = '+' if valor >= 0 else '-'
        print(f"  {variable:<15}  {signo}{abs(valor):.4f}  {barra}")


def guardar_heatmap(df: pd.DataFrame, ruta_docs: str) -> None:
    """Genera y guarda el heatmap de correlaciones en docs/correlaciones.png."""
    try:
        os.makedirs(ruta_docs, exist_ok=True)
        ruta_png = os.path.join(ruta_docs, 'correlaciones.png')

        columnas_numericas = COLUMNAS_ENTRADA + ['alerta_temperatura', 'alerta_luz',
                                                  'alerta_humedad_ambiente', 'riego']
        corr = df[columnas_numericas].corr()

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(
            corr,
            annot=True,
            fmt='.2f',
            cmap='RdYlGn',
            center=0,
            linewidths=0.5,
            ax=ax,
        )
        ax.set_title('Mapa de calor — Correlaciones EcoGrow', fontsize=14, pad=15)
        plt.tight_layout()
        fig.savefig(ruta_png, dpi=150)
        plt.close(fig)
        print(f"\n✓ Heatmap guardado en: {ruta_png}")
    except Exception as e:
        print(f"⚠ No se pudo guardar el heatmap: {e}")


def main():
    df = cargar_dataset(RUTA_DATASET)
    analizar_forma(df)
    analizar_nulos(df)
    distribucion_salidas(df)
    estadisticas_entradas(df)
    correlacion_con_riego(df)
    guardar_heatmap(df, RUTA_DOCS)
    print("\n✓ explorar_dataset.py ejecutado correctamente")


if __name__ == '__main__':
    main()
