import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder


RUTA_DATASET = os.path.join(os.path.dirname(__file__), '..', 'data', 'dataset_ecogrow_v2.csv')
RUTA_MODELO  = os.path.join(os.path.dirname(__file__), 'modelo_ecogrow.pkl')

COLUMNAS_X = ['temp', 'hum_amb', 'hum_suelo', 'luz', 'hora_dia']
COLUMNAS_Y = ['alerta_temperatura', 'alerta_luz', 'alerta_humedad_ambiente',
              'riego', 'estado_cultivo']


def cargar_datos(ruta: str):
    """Carga el dataset, codifica estado_cultivo y separa features de targets."""
    try:
        df = pd.read_csv(ruta)
    except FileNotFoundError:
        raise FileNotFoundError(f"Dataset no encontrado: {ruta}")

    # LabelEncoder para convertir texto → número (necesario para MultiOutputClassifier)
    le = LabelEncoder()
    df['estado_cultivo'] = le.fit_transform(df['estado_cultivo'])

    X = df[COLUMNAS_X]
    y = df[COLUMNAS_Y]
    return X, y, le


def dividir_datos(X: pd.DataFrame, y: pd.DataFrame):
    """Divide en conjuntos de entrenamiento y prueba."""
    return train_test_split(X, y, test_size=0.2, random_state=42)


def construir_modelo() -> MultiOutputClassifier:
    """Crea el clasificador multi-salida basado en árbol de decisión."""
    arbol = DecisionTreeClassifier(max_depth=5, random_state=42)
    return MultiOutputClassifier(arbol)


def evaluar_modelo(modelo: MultiOutputClassifier, X_test: pd.DataFrame,
                   y_test: pd.DataFrame, le: LabelEncoder) -> dict:
    """Predice sobre el conjunto de prueba e imprime métricas por salida."""
    y_pred = modelo.predict(X_test)
    y_pred_df = pd.DataFrame(y_pred, columns=COLUMNAS_Y, index=y_test.index)

    exactitudes = {}
    separador = '─' * 60

    for col in COLUMNAS_Y:
        real = y_test[col]
        pred = y_pred_df[col]
        acc  = accuracy_score(real, pred)
        exactitudes[col] = acc

        # Etiquetas de clase legibles para estado_cultivo
        target_names = [str(c) for c in le.classes_] if col == 'estado_cultivo' else None

        print(f"\n{separador}")
        print(f"  SALIDA: {col.upper()}")
        print(separador)
        print(f"  Exactitud (accuracy): {acc:.4f}  ({acc*100:.2f}%)")
        print("\n  Reporte de clasificación:")
        print(classification_report(real, pred, target_names=target_names, zero_division=0))
        print("  Matriz de confusión:")
        print(confusion_matrix(real, pred))

    return exactitudes


def guardar_modelo(modelo: MultiOutputClassifier, le: LabelEncoder, ruta: str) -> None:
    """Serializa el modelo y el encoder con joblib."""
    try:
        joblib.dump({'modelo': modelo, 'encoder_estado': le}, ruta)
        print(f"\n✓ Modelo guardado en: {ruta}")
    except Exception as e:
        print(f"⚠ No se pudo guardar el modelo: {e}")


def imprimir_tabla_resumen(exactitudes: dict) -> None:
    """Imprime una tabla con la exactitud de cada salida."""
    print("\n── TABLA RESUMEN DE EXACTITUDES ─────────────────────")
    print(f"  {'Salida':<30} {'Exactitud':>10}")
    print(f"  {'─'*30} {'─'*10}")
    for col, acc in exactitudes.items():
        print(f"  {col:<30} {acc:>9.4f}")
    promedio = sum(exactitudes.values()) / len(exactitudes)
    print(f"  {'─'*30} {'─'*10}")
    print(f"  {'PROMEDIO':<30} {promedio:>9.4f}")


def main():
    print("Cargando datos...")
    X, y, le = cargar_datos(RUTA_DATASET)

    print("Dividiendo datos (80% entrenamiento / 20% prueba)...")
    X_train, X_test, y_train, y_test = dividir_datos(X, y)
    print(f"  Entrenamiento: {len(X_train)} muestras")
    print(f"  Prueba:        {len(X_test)} muestras")

    print("\nEntrenando modelo multi-salida...")
    modelo = construir_modelo()
    modelo.fit(X_train, y_train)
    print("Modelo entrenado.")

    print("\nEvaluando modelo...")
    exactitudes = evaluar_modelo(modelo, X_test, y_test, le)

    imprimir_tabla_resumen(exactitudes)
    guardar_modelo(modelo, le, RUTA_MODELO)

    print("\n✓ entrenar_modelo.py ejecutado correctamente")


if __name__ == '__main__':
    main()
