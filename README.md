# 📊 SKINFIT - Procesamiento de Datos# SKINFIT - Análisis de Datos y Segmentación de Clientes



## 🚀 Uso Rápido## Descripción del Proyecto



```bashEste proyecto realiza un análisis completo de segmentación de clientes para SKINFIT, utilizando datos de sesiones de AgendaPro. El proceso se divide en dos etapas principales:

python RUN.py

```1. **Preprocesamiento y Consolidación** (`main.py`)

2. **Análisis ML y Segmentación** (`analisis_ml.py`)

Este comando ejecuta todo y genera `DatosCompletos.csv` listo para Google Looker.

## Flujo de Trabajo

---

### Paso 1: Preprocesamiento (`main.py`)

## 📁 Estructura del Proyecto

Este script toma el archivo original de sesiones y realiza:

### **Archivos de Entrada** (originales)

- `Base - Clientes.csv` - Datos de clientes- **Consolidación de atributos similares** usando fuzzy matching (umbral 85%)

- `Base - Sesiones.csv` - Datos de sesiones  - Ejemplo: "membresia", "membresía", "membresias" → "membresias" (la versión más frecuente)

- **Filtrado de columnas poco frecuentes** (apariciones < 0.5% del total)

### **Scripts** (numerados por orden de ejecución)- **One-hot encoding** de variables categóricas

1. **`RUN.py`** ⭐ - EJECUTAR ESTE (corre todo automáticamente)

2. `1_procesar_sesiones.py` - Procesa y binariza sesiones**Entrada:**

3. `2_procesar_clientes.py` - Agrega columna ID a clientes- `Base2 - Sesiones.csv` (datos originales con ~41,000 sesiones)

4. `3_hacer_join.py` - Une sesiones con clientes

5. `analisis_ml.py` - (Opcional) Segmentación de clientes con ML**Salida:**

- `datos_finales_transformados_y_reducidos.csv` (datos consolidados)

### **Archivos de Salida**

- **`DatosCompletos.csv`** ⭐ USAR ESTE EN LOOKER**Ejecución:**

- `SesionesFinal.csv` (intermedio)```bash

- `ClientesFinal.csv` (intermedio)python main.py

```

---

### Paso 2: Análisis ML (`analisis_ml.py`)

## ⚙️ ¿Qué Hace el Proceso?

Este script toma los datos consolidados y realiza:

### 1️⃣ Procesar Sesiones

- Consolida términos similares (ej: "membresia" + "membresía" → "membresias")- **Agregación a nivel de cliente** (de sesiones → clientes únicos)

- Convierte listas en columnas binarias (0/1)- **Segmentación de clientes** usando K-Means clustering (4 segmentos)

- Crea columnas: `tipo_tratamiento_*`, `productos_*`, `membresia_*`, etc.- **Modelo predictivo** para predecir frecuencia de visitas (Gradient Boosting)

- Agrega columna `ID` para identificar clientes- **Visualizaciones**:

  - Perfiles de segmentos

### 2️⃣ Procesar Clientes  - PCA de segmentos

- Agrega columna `ID` (usa email o nombre_apellido)  - Importancia de variables

- Elimina clientes duplicados  - Predicciones vs reales



### 3️⃣ Hacer JOIN**Entrada:**

- Une sesiones con datos de clientes por columna `ID`- `datos_finales_transformados_y_reducidos.csv`

- Incluye TODOS los clientes (con y sin sesiones)

**Salida:**

---- `output/clientes_segmentados.csv`

- `output/perfiles_segmentos_clientes.png`

## 📊 Archivo Final: DatosCompletos.csv- `output/pca_segmentacion_clientes.png`

- `output/importancia_variables_prediccion.png`

### Contenido:- `output/predicciones_vs_reales.png`

- **~43,000 filas** (sesiones + clientes sin sesiones)

- **~70 columnas** binarizadas**Ejecución:**

- **~18,000 clientes únicos**```bash

  - 16,000 con sesionespython analisis_ml.py

  - 2,000 sin sesiones```



### Columnas principales:## Ejemplo de Consolidación

- `ID` - Identificador único del cliente

- `fecha` - Fecha en formato ISO (YYYY-MM-DD)El script `main.py` consolida automáticamente variaciones similares:

- `Email`, `Nombres`, `Apellidos` - Datos del cliente

- `tipo_tratamiento_*` - Tratamientos (0/1)### Antes (datos originales):

- `productos_*` - Productos (0/1)```

- `membresia_*` - Membresías (0/1)recomendacion = ["membresia", "membresía", "membresias", "membresías", "membresia_silver"]

- `tipo_piel_*` - Tipos de piel (0/1)```

- `tolerancia_*` - Tolerancia (0/1)

### Después (consolidado):

---```

recomendacion_membresias  (consolida todas las variaciones de membresia/membresía)

## 🔧 Ejecutar Scripts Individualesrecomendacion_membresia_silver  (suficientemente diferente, se mantiene separada)

```

Si necesitas ejecutar solo una parte:

## Configuración

```bash

# Solo procesar sesiones### Umbral de Similitud (main.py)

python 1_procesar_sesiones.py```python

umbral_similitud = 85  # Porcentaje de similitud para consolidar términos

# Solo procesar clientes```

python 2_procesar_clientes.py

- **85%**: Captura variaciones como singular/plural, con/sin tildes

# Solo hacer el JOIN (requiere archivos intermedios)- **90%+**: Más estricto, solo variaciones muy similares

python 3_hacer_join.py- **80%-**: Más permisivo, puede consolidar términos diferentes



# Análisis ML opcional### Umbral de Frecuencia (main.py)

python analisis_ml.py```python

```umbral_frecuencia = 0.005  # 0.5% del total de filas

```

---

- Columnas que aparecen menos veces son descartadas

## 📈 Para Google Looker Studio- Con 41,000 sesiones, debe aparecer al menos ~206 veces



1. Sube `DatosCompletos.csv` a Looker### Número de Segmentos (analisis_ml.py)

2. Configura el tipo de datos:```python

   - `fecha` → Fecha (YYYY-MM-DD)n_customer_clusters = 4  # Número de segmentos de clientes

   - `ID` → Texto```

   - Columnas `*_*` → Número (0 o 1)

3. Listo para crear visualizaciones## Estructura de Archivos



### Ejemplos de análisis:```

```sqlSKINFIT/

-- Clientes únicos├── main.py                                    # Script de preprocesamiento

COUNT(DISTINCT ID)├── analisis_ml.py                             # Script de análisis ML

├── Base2 - Sesiones.csv                       # Datos originales

-- Clientes con sesiones├── datos_finales_transformados_y_reducidos.csv # Datos consolidados

COUNT(DISTINCT ID) WHERE fecha IS NOT NULL├── output/

│   ├── clientes_segmentados.csv

-- Tratamientos más populares│   ├── perfiles_segmentos_clientes.png

SUM(tipo_tratamiento_hydra), SUM(tipo_tratamiento_detox), etc.│   ├── pca_segmentacion_clientes.png

│   ├── importancia_variables_prediccion.png

-- Productos más recomendados│   └── predicciones_vs_reales.png

SUM(productos_retinol), SUM(productos_mascarilla_calmante), etc.└── README.md

``````



---## Dependencias



## ⚙️ Configuración (Opcional)```bash

pip install pandas numpy matplotlib seaborn scikit-learn rapidfuzz openpyxl

Puedes ajustar parámetros en `1_procesar_sesiones.py`:```



```python## Notas Importantes

umbral_frecuencia = 0.005  # Columnas con <0.5% se descartan

umbral_similitud = 85      # % similitud para fuzzy matching1. **Orden de ejecución**: Siempre ejecutar `main.py` primero para generar el archivo consolidado

```2. **Datos originales**: Mantener `Base2 - Sesiones.csv` sin modificar

3. **Consolidación**: La función `consolidar_atributos()` usa `rapidfuzz` para identificar términos similares

---4. **Performance**: Con ~8,000 clientes y ~90 características, el clustering toma pocos segundos



## 📝 Dependencias## Preguntas Frecuentes



```bash### ¿Por qué hay menos clientes que sesiones?

pip install pandas rapidfuzz openpyxl

```Las ~41,000 filas en el archivo original representan **sesiones individuales**. Cada cliente puede tener múltiples sesiones. Al agrupar por email, obtenemos ~8,000 **clientes únicos**.



Para análisis ML (opcional):Ejemplo:

```bash- `cliente@example.com` tiene 5 sesiones → se cuenta como 1 cliente con `num_sesiones=5`

pip install scikit-learn matplotlib seaborn

```### ¿Cómo funciona la consolidación?



---El algoritmo usa **fuzzy string matching** para medir la similitud entre términos:



## 🆘 Solución de Problemas1. Extrae todos los términos únicos de una columna

2. Para cada término, encuentra otros similares (>85% de similitud)

### Error: "No se encontró el archivo"3. Agrupa los términos similares

Verifica que existan:4. Elige el término más frecuente como "canónico"

- `Base - Clientes.csv`

- `Base - Sesiones.csv`Ejemplo:

- Términos: ["membresia" (100x), "membresía" (50x), "membresias" (80x)]

### El archivo es muy grande- Similitud: membresia ↔ membresía = 89%, membresia ↔ membresias = 95%

El script ya optimiza el tamaño:- Resultado: Todos se consolidan como "membresia" (la más frecuente)

- Solo incluye Email, Nombres, Apellidos de clientes

- Descarta columnas poco frecuentes (<0.5%)### ¿Cómo ajustar el número de segmentos?

- Resultado: ~20 MB (manejable para Looker/Sheets)

Edita `analisis_ml.py`:

### Fechas no se ven bien```python

Ya están en formato ISO (YYYY-MM-DD).config = {

En Looker: Campo → Tipo → Fecha    "n_customer_clusters": 4,  # Cambia este valor

    ...

---}

```

**Última actualización:** Octubre 2025  

**Versión:** 3.0 - SimplificadaPuedes probar con 3, 4, 5, o más segmentos. El valor óptimo depende de tus objetivos de negocio.


## Contacto

Para preguntas o problemas, contactar al equipo de análisis de datos de SKINFIT.
