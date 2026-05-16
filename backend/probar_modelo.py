import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

import joblib
import pandas as pd


RUTA_MODELO = os.path.join(os.path.dirname(__file__), 'modelo_ecogrow.pkl')

COLUMNAS_X = ['temp', 'hum_amb', 'hum_suelo', 'luz', 'hora_dia']
COLUMNAS_Y = ['alerta_temperatura', 'alerta_luz', 'alerta_humedad_ambiente',
              'riego', 'estado_cultivo']

# Mapeos de etiquetas legibles en español para salidas numéricas
ETIQUETAS = {
    'alerta_temperatura': {
        0: 'Sin alerta',
        1: 'Alerta leve',
        2: 'Alerta severa',
    },
    'alerta_luz': {
        0: 'Sin alerta',
        1: 'Poca luz',
        2: 'Luz insuficiente',
    },
    'alerta_humedad_ambiente': {
        0: 'Sin alerta',
        1: 'Alerta leve',
        2: 'Alerta severa',
    },
    'riego': {
        0: 'No',
        1: 'Sí',
    },
}

ESCENARIOS = [
    {
        'nombre': 'Planta en estrés severo',
        'datos':  {'temp': 38, 'hum_amb': 25, 'hum_suelo': 150, 'luz': 50, 'hora_dia': 14},
    },
    {
        'nombre': 'Condiciones óptimas',
        'datos':  {'temp': 22, 'hum_amb': 60, 'hum_suelo': 650, 'luz': 800, 'hora_dia': 10},
    },
    {
        'nombre': 'Tarde con suelo seco',
        'datos':  {'temp': 20, 'hum_amb': 55, 'hum_suelo': 320, 'luz': 400, 'hora_dia': 18},
    },
]


def cargar_modelo(ruta: str):
    """Carga el dict {modelo, encoder_estado} serializado desde disco."""
    try:
        paquete = joblib.load(ruta)
        return paquete['modelo'], paquete['encoder_estado']
    except FileNotFoundError:
        raise FileNotFoundError(f"Modelo no encontrado en: {ruta}\n"
                                "Ejecuta primero entrenar_modelo.py")
    except Exception as e:
        raise RuntimeError(f"Error al cargar el modelo: {e}")


def predecir_escenario(modelo, le, datos: dict) -> dict:
    """Recibe un dict con los valores de entrada y devuelve las predicciones."""
    fila = pd.DataFrame([datos], columns=COLUMNAS_X)
    pred = modelo.predict(fila)[0]
    predicciones = dict(zip(COLUMNAS_Y, pred))

    # Decodificar estado_cultivo (número → texto original)
    predicciones['estado_cultivo'] = le.inverse_transform(
        [int(predicciones['estado_cultivo'])]
    )[0]
    return predicciones


def traducir(predicciones: dict) -> dict:
    """Convierte los valores numéricos en etiquetas legibles en español."""
    resultado = {}
    for col, val in predicciones.items():
        if col == 'estado_cultivo':
            resultado[col] = str(val)
        else:
            resultado[col] = ETIQUETAS[col].get(int(val), str(val))
    return resultado


def imprimir_reporte(numero: int, nombre: str, datos: dict, resultado: dict) -> None:
    """Imprime el reporte legible de un escenario."""
    separador = '═' * 56
    print(f"\n{separador}")
    print(f"  === Escenario {numero}: {nombre} ===")
    print(separador)
    print(f"  Temp: {datos['temp']}°C | "
          f"Hum. amb: {datos['hum_amb']}% | "
          f"Hum. suelo: {datos['hum_suelo']} | "
          f"Luz: {datos['luz']} | "
          f"Hora: {datos['hora_dia']}h")
    print(f"  → Alerta temperatura : {resultado['alerta_temperatura']}")
    print(f"  → Alerta luz         : {resultado['alerta_luz']}")
    print(f"  → Alerta hum. amb.   : {resultado['alerta_humedad_ambiente']}")
    print(f"  → Riego necesario    : {resultado['riego']}")
    print(f"  → Estado del cultivo : {resultado['estado_cultivo']}")
    print(separador)


def main():
    modelo, le = cargar_modelo(RUTA_MODELO)

    for i, escenario in enumerate(ESCENARIOS, start=1):
        predicciones = predecir_escenario(modelo, le, escenario['datos'])
        resultado    = traducir(predicciones)
        imprimir_reporte(i, escenario['nombre'], escenario['datos'], resultado)

    print("\n✓ probar_modelo.py ejecutado correctamente")


if __name__ == '__main__':
    main()
