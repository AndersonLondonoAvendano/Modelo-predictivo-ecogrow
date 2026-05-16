import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

import joblib
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree, export_text


RUTA_MODELO = os.path.join(os.path.dirname(__file__), 'modelo_ecogrow.pkl')
RUTA_DOCS   = os.path.join(os.path.dirname(__file__), '..', 'docs')

NOMBRES_FEATURES = ['temp', 'hum_amb', 'hum_suelo', 'luz', 'hora_dia']
COLUMNAS_Y = ['alerta_temperatura', 'alerta_luz', 'alerta_humedad_ambiente',
              'riego', 'estado_cultivo']


def cargar_modelo(ruta: str):
    """Carga el dict {modelo, encoder_estado} serializado desde disco."""
    try:
        paquete = joblib.load(ruta)
        modelo  = paquete['modelo']
        le      = paquete['encoder_estado']
        print(f"Modelo cargado desde: {ruta}")
        return modelo, le
    except FileNotFoundError:
        raise FileNotFoundError(f"Modelo no encontrado: {ruta}\n"
                                "Ejecuta primero entrenar_modelo.py")
    except Exception as e:
        raise RuntimeError(f"Error al cargar el modelo: {e}")


def guardar_imagenes_arboles(modelo, le, ruta_docs: str) -> None:
    """Genera y guarda una imagen PNG por cada árbol de decisión."""
    os.makedirs(ruta_docs, exist_ok=True)

    for estimador, nombre_salida in zip(modelo.estimators_, COLUMNAS_Y):
        ruta_png = os.path.join(ruta_docs, f'arbol_{nombre_salida}.png')
        try:
            # Clases en texto: para estado_cultivo usamos las etiquetas originales
            if nombre_salida == 'estado_cultivo':
                class_names = [str(c) for c in le.classes_]
            else:
                class_names = [str(c) for c in estimador.classes_]

            fig, ax = plt.subplots(figsize=(20, 10))
            plot_tree(
                estimador,
                filled=True,
                max_depth=3,
                feature_names=NOMBRES_FEATURES,
                class_names=class_names,
                ax=ax,
                fontsize=9,
                impurity=False,
                precision=2,
            )
            ax.set_title(f'Árbol de decisión — {nombre_salida}', fontsize=14, pad=15)
            plt.tight_layout()
            fig.savefig(ruta_png, dpi=120)
            plt.close(fig)
            print(f"  ✓ {ruta_png}")
        except Exception as e:
            print(f"  ⚠ No se pudo guardar {ruta_png}: {e}")


def guardar_arboles_texto(modelo, le, ruta_docs: str) -> None:
    """Exporta todos los árboles en formato texto a docs/arboles_texto.txt."""
    os.makedirs(ruta_docs, exist_ok=True)
    ruta_txt = os.path.join(ruta_docs, 'arboles_texto.txt')
    try:
        with open(ruta_txt, 'w', encoding='utf-8') as f:
            f.write("ÁRBOLES DE DECISIÓN — MODELO ECOGROW\n")
            f.write("=" * 60 + "\n\n")
            for estimador, nombre_salida in zip(modelo.estimators_, COLUMNAS_Y):
                f.write(f"{'─'*60}\n")
                f.write(f"  SALIDA: {nombre_salida.upper()}\n")
                if nombre_salida == 'estado_cultivo':
                    f.write(f"  Clases: {list(le.classes_)}\n")
                f.write(f"{'─'*60}\n")
                texto = export_text(
                    estimador,
                    feature_names=NOMBRES_FEATURES,
                    max_depth=10,
                )
                f.write(texto)
                f.write("\n")
        print(f"\n✓ Árboles en texto guardados en: {ruta_txt}")
    except Exception as e:
        print(f"⚠ No se pudo guardar {ruta_txt}: {e}")


def guardar_importancia_features(modelo, ruta_docs: str) -> None:
    """Guarda en docs/feature_importance.txt la variable más determinante por salida."""
    os.makedirs(ruta_docs, exist_ok=True)
    ruta_txt = os.path.join(ruta_docs, 'feature_importance.txt')
    try:
        with open(ruta_txt, 'w', encoding='utf-8') as f:
            f.write("IMPORTANCIA DE VARIABLES — MODELO ECOGROW\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"  {'Salida':<30} {'Variable más determinante':<20} {'Importancia':>10}\n")
            f.write(f"  {'─'*30} {'─'*20} {'─'*10}\n")

            for estimador, nombre_salida in zip(modelo.estimators_, COLUMNAS_Y):
                importancias = estimador.feature_importances_
                idx_max      = importancias.argmax()
                mejor_feat   = NOMBRES_FEATURES[idx_max]
                mejor_val    = importancias[idx_max]
                f.write(f"  {nombre_salida:<30} {mejor_feat:<20} {mejor_val:>9.4f}\n")

                f.write(f"\n  Detalle — {nombre_salida}:\n")
                pares = sorted(zip(NOMBRES_FEATURES, importancias), key=lambda x: x[1], reverse=True)
                for feat, imp in pares:
                    barra = '█' * int(imp * 30)
                    f.write(f"    {feat:<15}  {imp:.4f}  {barra}\n")
                f.write("\n")

        print(f"✓ Importancia de features guardada en: {ruta_txt}")
    except Exception as e:
        print(f"⚠ No se pudo guardar {ruta_txt}: {e}")


def main():
    modelo, le = cargar_modelo(RUTA_MODELO)

    print("\nGenerando imágenes PNG de los árboles...")
    guardar_imagenes_arboles(modelo, le, RUTA_DOCS)

    print("\nExportando árboles en texto...")
    guardar_arboles_texto(modelo, le, RUTA_DOCS)

    print("\nCalculando importancia de variables...")
    guardar_importancia_features(modelo, RUTA_DOCS)

    print("\n✓ visualizar_arbol.py ejecutado correctamente")


if __name__ == '__main__':
    main()
