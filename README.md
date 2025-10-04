# SKINFIT - Análisis de Datos y Segmentación de Clientes

## Descripción del Proyecto

Este proyecto realiza un análisis completo de segmentación de clientes para SKINFIT, utilizando datos de sesiones de AgendaPro. El proceso se divide en dos etapas principales:

1. **Preprocesamiento y Consolidación** (`main.py`)
2. **Análisis ML y Segmentación** (`analisis_ml.py`)

## Flujo de Trabajo

### Paso 1: Preprocesamiento (`main.py`)

Este script toma el archivo original de sesiones y realiza:

- **Consolidación de atributos similares** usando fuzzy matching (umbral 85%)
  - Ejemplo: "membresia", "membresía", "membresias" → "membresias" (la versión más frecuente)
- **Filtrado de columnas poco frecuentes** (apariciones < 0.5% del total)
- **One-hot encoding** de variables categóricas

**Entrada:**
- `Base2 - Sesiones.csv` (datos originales con ~41,000 sesiones)

**Salida:**
- `datos_finales_transformados_y_reducidos.csv` (datos consolidados)

**Ejecución:**
```bash
python main.py
```

### Paso 2: Análisis ML (`analisis_ml.py`)

Este script toma los datos consolidados y realiza:

- **Agregación a nivel de cliente** (de sesiones → clientes únicos)
- **Segmentación de clientes** usando K-Means clustering (4 segmentos)
- **Modelo predictivo** para predecir frecuencia de visitas (Gradient Boosting)
- **Visualizaciones**:
  - Perfiles de segmentos
  - PCA de segmentos
  - Importancia de variables
  - Predicciones vs reales

**Entrada:**
- `datos_finales_transformados_y_reducidos.csv`

**Salida:**
- `output/clientes_segmentados.csv`
- `output/perfiles_segmentos_clientes.png`
- `output/pca_segmentacion_clientes.png`
- `output/importancia_variables_prediccion.png`
- `output/predicciones_vs_reales.png`

**Ejecución:**
```bash
python analisis_ml.py
```

## Ejemplo de Consolidación

El script `main.py` consolida automáticamente variaciones similares:

### Antes (datos originales):
```
recomendacion = ["membresia", "membresía", "membresias", "membresías", "membresia_silver"]
```

### Después (consolidado):
```
recomendacion_membresias  (consolida todas las variaciones de membresia/membresía)
recomendacion_membresia_silver  (suficientemente diferente, se mantiene separada)
```

## Configuración

### Umbral de Similitud (main.py)
```python
umbral_similitud = 85  # Porcentaje de similitud para consolidar términos
```

- **85%**: Captura variaciones como singular/plural, con/sin tildes
- **90%+**: Más estricto, solo variaciones muy similares
- **80%-**: Más permisivo, puede consolidar términos diferentes

### Umbral de Frecuencia (main.py)
```python
umbral_frecuencia = 0.005  # 0.5% del total de filas
```

- Columnas que aparecen menos veces son descartadas
- Con 41,000 sesiones, debe aparecer al menos ~206 veces

### Número de Segmentos (analisis_ml.py)
```python
n_customer_clusters = 4  # Número de segmentos de clientes
```

## Estructura de Archivos

```
SKINFIT/
├── main.py                                    # Script de preprocesamiento
├── analisis_ml.py                             # Script de análisis ML
├── Base2 - Sesiones.csv                       # Datos originales
├── datos_finales_transformados_y_reducidos.csv # Datos consolidados
├── output/
│   ├── clientes_segmentados.csv
│   ├── perfiles_segmentos_clientes.png
│   ├── pca_segmentacion_clientes.png
│   ├── importancia_variables_prediccion.png
│   └── predicciones_vs_reales.png
└── README.md
```

## Dependencias

```bash
pip install pandas numpy matplotlib seaborn scikit-learn rapidfuzz openpyxl
```

## Notas Importantes

1. **Orden de ejecución**: Siempre ejecutar `main.py` primero para generar el archivo consolidado
2. **Datos originales**: Mantener `Base2 - Sesiones.csv` sin modificar
3. **Consolidación**: La función `consolidar_atributos()` usa `rapidfuzz` para identificar términos similares
4. **Performance**: Con ~8,000 clientes y ~90 características, el clustering toma pocos segundos

## Preguntas Frecuentes

### ¿Por qué hay menos clientes que sesiones?

Las ~41,000 filas en el archivo original representan **sesiones individuales**. Cada cliente puede tener múltiples sesiones. Al agrupar por email, obtenemos ~8,000 **clientes únicos**.

Ejemplo:
- `cliente@example.com` tiene 5 sesiones → se cuenta como 1 cliente con `num_sesiones=5`

### ¿Cómo funciona la consolidación?

El algoritmo usa **fuzzy string matching** para medir la similitud entre términos:

1. Extrae todos los términos únicos de una columna
2. Para cada término, encuentra otros similares (>85% de similitud)
3. Agrupa los términos similares
4. Elige el término más frecuente como "canónico"

Ejemplo:
- Términos: ["membresia" (100x), "membresía" (50x), "membresias" (80x)]
- Similitud: membresia ↔ membresía = 89%, membresia ↔ membresias = 95%
- Resultado: Todos se consolidan como "membresia" (la más frecuente)

### ¿Cómo ajustar el número de segmentos?

Edita `analisis_ml.py`:
```python
config = {
    "n_customer_clusters": 4,  # Cambia este valor
    ...
}
```

Puedes probar con 3, 4, 5, o más segmentos. El valor óptimo depende de tus objetivos de negocio.

## Contacto

Para preguntas o problemas, contactar al equipo de análisis de datos de SKINFIT.
