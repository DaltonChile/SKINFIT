import pandas as pd
import ast
from rapidfuzz import process, fuzz
from collections import Counter

# --- FUNCIONES AUXILIARES (Necesarias para la transformación) ---

def parsear_lista_segura(valor):
    """Convierte de forma segura un string con formato de lista a una lista real de Python."""
    try:
        if isinstance(valor, str) and valor.startswith('[') and valor.endswith(']'):
            return ast.literal_eval(valor)
        return []
    except (ValueError, SyntaxError):
        return []

def consolidar_atributos(series, umbral_similitud=85):
    """Analiza una columna, extrae todos los atributos y agrupa los similares."""
    todos_los_items = [
        item.strip().lower() for sublista in series 
        for item in sublista if isinstance(item, str)
    ]
    if not todos_los_items:
        return {}, []
    frecuencias = Counter(todos_los_items)
    items_unicos = sorted(list(frecuencias.keys()))
    mapeo = {}
    items_ya_procesados = set()
    for item in items_unicos:
        if item in items_ya_procesados:
            continue
        opciones = [u for u in items_unicos if u not in items_ya_procesados]
        coincidencias = process.extract(item, opciones, scorer=fuzz.ratio, score_cutoff=umbral_similitud)
        grupo_similar = [coincidencia[0] for coincidencia in coincidencias]
        nombre_canonico = max(grupo_similar, key=lambda x: frecuencias.get(x, 0))
        for item_similar in grupo_similar:
            mapeo[item_similar] = nombre_canonico
            items_ya_procesados.add(item_similar)
    lista_canonica = sorted(list(set(mapeo.values())))
    return mapeo, lista_canonica

# --- SCRIPT PRINCIPAL "TODO EN UNO" ---

# 1. Configuración
archivo_entrada = 'Base2 - Sesiones.csv'  # <-- El archivo ORIGINAL
archivo_salida = 'datos_finales_transformados_y_reducidos.csv'

columnas_a_procesar = [
    'tipo_tratamiento',
    'problemas_piel',
    'zonas_tratadas',
    'productos',
]

# Umbral de relevancia (0.005 = 0.5%)
umbral_frecuencia = 0.005

# 2. Carga de Datos Originales
try:
    df = pd.read_csv(archivo_entrada)
    print(f"Archivo original '{archivo_entrada}' cargado. Dimensiones: {df.shape}")
except FileNotFoundError:
    print(f"Error: No se pudo encontrar el archivo '{archivo_entrada}'.")
    exit()

# 3. Proceso de Transformación y Filtrado Integrado
num_filas = len(df)
min_apariciones = int(num_filas * umbral_frecuencia)
print(f"Una columna nueva se mantendrá si aparece al menos {min_apariciones} veces (umbral del {umbral_frecuencia*100}%).")

# Lista para guardar solo las nuevas columnas que SÍ cumplen el requisito
columnas_nuevas_relevantes = []
total_columnas_generadas = 0
total_columnas_descartadas = 0

for columna in columnas_a_procesar:
    if columna in df.columns:
        print(f"\n  - Procesando columna original: '{columna}'")
        series_parseada = df[columna].apply(parsear_lista_segura)
        mapeo, atributos_canonicos = consolidar_atributos(series_parseada)

        if not atributos_canonicos:
            print("    -> No se encontraron atributos.")
            continue

        for atributo in atributos_canonicos:
            total_columnas_generadas += 1
            nueva_columna_nombre = f"{columna}_{atributo.replace(' ', '_')}"
            
            # Genera la nueva columna en memoria
            nueva_serie = series_parseada.apply(
                lambda lista_items: 1 if any(mapeo.get(str(item).strip().lower()) == atributo for item in lista_items) else 0
            )
            nueva_serie.name = nueva_columna_nombre

            # **FILTRADO INMEDIATO**: Comprueba si la columna es relevante
            if nueva_serie.sum() >= min_apariciones:
                columnas_nuevas_relevantes.append(nueva_serie)
                # print(f"    -> Se MANTIENE '{nueva_columna_nombre}' (Aparece {nueva_serie.sum()} veces)")
            else:
                total_columnas_descartadas += 1
                # print(f"    -> Se DESCARTA '{nueva_columna_nombre}' (Aparece solo {nueva_serie.sum()} veces)")


# 4. Ensamblaje Final
# Tomamos el DataFrame original y eliminamos las columnas que procesamos
df_base = df.drop(columns=[col for col in columnas_a_procesar if col in df.columns])

# Unimos el DataFrame base con la lista de nuevas columnas que sí pasaron el filtro
df_final = pd.concat([df_base] + columnas_nuevas_relevantes, axis=1)

print("\n--- RESUMEN DEL PROCESO ---")
print(f"Se generaron y evaluaron un total de {total_columnas_generadas} columnas nuevas.")
print(f"Se mantuvieron {len(columnas_nuevas_relevantes)} columnas por ser relevantes.")
print(f"Se descartaron {total_columnas_descartadas} columnas por baja frecuencia.")
print(f"Dimensiones finales del archivo: {df_final.shape}")

# 5. Guardado del Resultado
df_final.to_csv(archivo_salida, index=False, encoding='utf-8-sig')
print(f"\n¡Proceso completado! ✨ El archivo final ha sido guardado como '{archivo_salida}'.")