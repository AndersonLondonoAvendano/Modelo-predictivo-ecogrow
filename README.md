# Guía de Integración del Modelo de IA — EcoGrow
## Para el desarrollador del backend (Flask/app.py)

---

## Contexto: qué cambió en el modelo

El modelo de IA que se entrenó **no predice solo si regar o no**. Predice **5 cosas al mismo tiempo** con una sola llamada. Esto cambia cómo el backend debe cargar el modelo, qué datos debe pasarle y qué respuesta debe esperar.

El archivo del modelo ya no es `modelo_riego.pkl` — ahora es `backend/modelo_ecogrow.pkl`.

---

## 1. Qué recibe el modelo y qué devuelve

### Entradas — los 5 valores del sensor (siempre en este orden exacto):

| Campo       | Descripción                        | Ejemplo |
|-------------|-------------------------------------|---------|
| `temp`      | Temperatura en °C                  | 24.5    |
| `hum_amb`   | Humedad ambiental en %             | 62.0    |
| `hum_suelo` | Humedad del suelo (valor analógico 0-1023) | 310.0 |
| `luz`       | Nivel de luz (valor analógico 0-1023) | 750.0 |
| `hora_dia`  | Hora actual del día (0-23, entero) | 9       |

> **Importante:** el orden es fijo. Si los pasas en otro orden el modelo predice basura sin dar ningún error. Siempre usar exactamente: `[temp, hum_amb, hum_suelo, luz, hora_dia]`

### Salidas — lo que devuelve el modelo:

| Campo                     | Tipo     | Valores posibles              | Significado |
|---------------------------|----------|-------------------------------|-------------|
| `alerta_temperatura`      | Número   | 0, 1, 2                       | 0=sin alerta, 1=alerta leve, 2=alerta severa |
| `alerta_luz`              | Número   | 0, 1, 2                       | 0=luz suficiente, 1=poca luz, 2=luz insuficiente |
| `alerta_humedad_ambiente` | Número   | 0, 1, 2                       | 0=normal, 1=aire seco, 2=riesgo de hongos |
| `riego`                   | Número   | 0, 1                          | 0=no regar, 1=regar |
| `estado_cultivo`          | Texto    | 'optimo', 'estres_leve', 'estres_severo' | Estado general del cultivo |

---

## 2. Cambios exactos en app.py

### 2.1 Cambiar la carga del modelo

**Antes (lo que tenías):**
```python
modelo = joblib.load('backend/modelo_riego.pkl')
```

**Ahora:**
```python
modelo = joblib.load('backend/modelo_ecogrow.pkl')
```

---

### 2.2 Reemplazar la función de predicción completa

**La función anterior solo predecía riego (0 o 1). Esta es la nueva:**

```python
# Mapas para traducir números a texto legible
MAPA_ALERTA = {0: 'Sin alerta', 1: 'Alerta leve', 2: 'Alerta severa'}
MAPA_ALERTA_LUZ = {0: 'Luz suficiente', 1: 'Poca luz', 2: 'Luz insuficiente'}
MAPA_ALERTA_HUM = {0: 'Normal', 1: 'Aire muy seco', 2: 'Riesgo de hongos'}
MAPA_RIEGO = {0: 'No regar', 1: 'Activar riego'}

def realizar_prediccion(datos):
    """
    Recibe el diccionario de datos del sensor y agrega las 5 predicciones
    del modelo directamente al mismo diccionario.
    """
    try:
        # ORDEN FIJO — no cambiar este orden
        entrada = [[
            float(datos['temp']),
            float(datos['hum']),       # hum_amb en el dataset
            float(datos['suelo']),     # hum_suelo en el dataset
            float(datos['luz']),
            int(datetime.now().hour)   # hora_dia
        ]]

        # El modelo devuelve un array con las 5 predicciones
        predicciones = modelo.predict(entrada)[0]

        # Obtener probabilidad de riego (índice 3 = columna riego)
        prob_riego = modelo.estimators_[3].predict_proba(entrada)[0]
        # predict_proba devuelve [prob_clase_0, prob_clase_1]
        porcentaje_riego = round(prob_riego[1] * 100, 1) if len(prob_riego) > 1 else 0.0

        # Asignar cada predicción al diccionario de datos
        datos['pred_alerta_temp']     = int(predicciones[0])
        datos['pred_alerta_luz']      = int(predicciones[1])
        datos['pred_alerta_hum_amb']  = int(predicciones[2])
        datos['pred_riego']           = int(predicciones[3])
        datos['pred_estado_cultivo']  = str(predicciones[4])
        datos['prob_riego_pct']       = porcentaje_riego

        # Versiones en texto para mostrar en el dashboard
        datos['texto_alerta_temp']    = MAPA_ALERTA.get(int(predicciones[0]), 'Desconocido')
        datos['texto_alerta_luz']     = MAPA_ALERTA_LUZ.get(int(predicciones[1]), 'Desconocido')
        datos['texto_alerta_hum_amb'] = MAPA_ALERTA_HUM.get(int(predicciones[2]), 'Desconocido')
        datos['texto_riego']          = MAPA_RIEGO.get(int(predicciones[3]), 'Desconocido')

        # Enviar comando físico al Arduino según predicción de riego
        if int(predicciones[3]) == 1:
            # El modelo dice que hay que regar
            enviar_comando_serial('R')
        else:
            # El modelo dice que no hay que regar
            enviar_comando_serial('S')

    except Exception as e:
        print(f"Error al realizar predicción: {e}")
```

> **Nota:** los campos del JSON que envía el Arduino son `temp`, `hum`, `suelo`, `luz` (según el sketch .ino que escribió el otro integrante). El modelo fue entrenado con columnas llamadas `temp`, `hum_amb`, `hum_suelo`, `luz`. Al pasarlos como array en el orden correcto, el nombre no importa — solo el orden.

---

### 2.3 Actualizar la ruta /predict

**Antes devolvía solo:**
```json
{"prediccion": 1, "probabilidad": 0.82, "accion": "Activar riego"}
```

**Ahora debe devolver todo esto:**

```python
@app.route('/predict')
def predict():
    """Retorna la predicción completa del modelo con todas las alertas."""
    if not ultimos_datos:
        return jsonify({'error': 'Sin datos del sensor aún'}), 404

    return jsonify({
        # Predicciones numéricas (para lógica en el frontend)
        'pred_riego':           ultimos_datos.get('pred_riego', 0),
        'pred_alerta_temp':     ultimos_datos.get('pred_alerta_temp', 0),
        'pred_alerta_luz':      ultimos_datos.get('pred_alerta_luz', 0),
        'pred_alerta_hum_amb':  ultimos_datos.get('pred_alerta_hum_amb', 0),
        'pred_estado_cultivo':  ultimos_datos.get('pred_estado_cultivo', 'sin_datos'),

        # Textos legibles (para mostrar directo en el dashboard)
        'texto_riego':          ultimos_datos.get('texto_riego', 'Sin datos'),
        'texto_alerta_temp':    ultimos_datos.get('texto_alerta_temp', 'Sin datos'),
        'texto_alerta_luz':     ultimos_datos.get('texto_alerta_luz', 'Sin datos'),
        'texto_alerta_hum_amb': ultimos_datos.get('texto_alerta_hum_amb', 'Sin datos'),

        # Probabilidad de riego en porcentaje (para la barra del dashboard)
        'prob_riego_pct':       ultimos_datos.get('prob_riego_pct', 0.0),

        # Valores del sensor que generaron esta predicción (para auditoría)
        'sensor_temp':          ultimos_datos.get('temp', None),
        'sensor_hum_amb':       ultimos_datos.get('hum', None),
        'sensor_hum_suelo':     ultimos_datos.get('suelo', None),
        'sensor_luz':           ultimos_datos.get('luz', None),
        'hora_prediccion':      ultimos_datos.get('ts', None),
    })
```

---

### 2.4 Actualizar registro.csv

Las columnas del CSV donde se guarda el historial deben incluir las nuevas predicciones:

```python
# Cabeceras del CSV — reemplazar las anteriores
CABECERAS_CSV = [
    'timestamp',
    'temp', 'hum_amb', 'hum_suelo', 'luz', 'hora_dia',
    'pred_alerta_temp', 'pred_alerta_luz', 'pred_alerta_hum_amb',
    'pred_riego', 'pred_estado_cultivo', 'prob_riego_pct'
]
```

---

## 3. Verificar que la integración funciona

Una vez hechos los cambios, probar con curl o Postman sin el Arduino conectado (modo simulación):

```bash
# Verificar que el servidor arranca sin errores
python backend/app.py

# En otra terminal, consultar la predicción
curl http://localhost:5000/predict

# Respuesta esperada (con datos simulados):
# {
#   "pred_riego": 1,
#   "pred_alerta_temp": 0,
#   "pred_alerta_luz": 0,
#   "pred_alerta_hum_amb": 1,
#   "pred_estado_cultivo": "estres_leve",
#   "texto_riego": "Activar riego",
#   "prob_riego_pct": 87.3,
#   ...
# }
```

Si el servidor arranca con un error como `FileNotFoundError: modelo_ecogrow.pkl`, significa que el modelo aún no ha sido entrenado. Avisar al integrante de IA para que ejecute primero `python backend/entrenar_modelo.py`.

---

## 4. Resumen de cambios en una línea por cada uno

| Qué cambiar | Qué hacer |
|-------------|-----------|
| Nombre del archivo del modelo | `modelo_riego.pkl` → `modelo_ecogrow.pkl` |
| Función `realizar_prediccion()` | Reemplazar completamente con la nueva versión |
| Ruta `/predict` | Ampliar la respuesta JSON con los 9 campos nuevos |
| Cabeceras de `registro.csv` | Agregar las 6 columnas de predicción nuevas |
| Comando al Arduino | Sin cambios — sigue siendo 'R' y 'S' |
| Puerto serial | Sin cambios |
| Rutas `/data`, `/history`, `/status`, `/comando` | Sin cambios |

---

## 5. Dependencia de entrega

```
[Anderson — modelo]          [Daniel/Juan — backend]
entrenar_modelo.py     →     modelo_ecogrow.pkl disponible
probar_modelo.py       →     verificar que predice bien
                       →     copiar función realizar_prediccion()
                       →     actualizar /predict
                       →     probar con curl
```