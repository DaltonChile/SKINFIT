# 📊 SKINFIT - Pipeline de Datos

## 🚀 Inicio Rápido

### Opción 1: Ejecutar todo automáticamente
```bash
python ejecutar_todo.py
```
Este comando ejecuta todo el pipeline y genera los 3 archivos finales.

### Opción 2: Ejecutar paso a paso
```bash
python main.py                  # 1. Procesa sesiones
python procesar_clientes.py     # 2. Procesa clientes  
python verificar_join.py        # 3. Verifica compatibilidad
python hacer_join.py            # 4. Hace el JOIN
```

---

## 📁 Archivos del Proyecto

### **Archivos de Entrada** (originales)
- `Base - Sesiones.csv` - Sesiones originales de AgendaPro (~41k filas)
- `Base - Clientes.csv` - Clientes originales de AgendaPro

### **Scripts de Procesamiento**
| Script | Qué hace | Input | Output |
|--------|----------|-------|--------|
| `main.py` | Procesa sesiones: consolidación fuzzy + transformación | `Base - Sesiones.csv` | `SesionesFinal.csv` |
| `procesar_clientes.py` | Agrega columna ID a clientes | `Base - Clientes.csv` | `ClientesFinal.csv` |
| `verificar_join.py` | Verifica que los IDs coincidan | Ambos archivos finales | Reporte en consola |
| `hacer_join.py` | Une sesiones y clientes por ID | `SesionesFinal.csv` + `ClientesFinal.csv` | `DatosCompletos.csv` |
| `ejecutar_todo.py` | **Ejecuta todo el pipeline automáticamente** | Archivos originales | Todos los archivos finales |

### **Archivos de Salida** (procesados)
- ✅ `SesionesFinal.csv` - Sesiones procesadas con columnas consolidadas y columna ID
- ✅ `ClientesFinal.csv` - Clientes con columna ID
- ✅ `DatosCompletos.csv` - **Archivo final con JOIN completo** (listo para Looker)

---

## 🔑 Columna ID

La columna **ID** se crea con esta lógica en ambos archivos:

1. **Primera prioridad:** Email (si existe)
   - Ejemplo: `juan@gmail.com`

2. **Segunda prioridad:** Nombre_Apellido (si no hay email)
   - Ejemplo: `maria_lopez`

3. **Tercera prioridad:** sin_id_123 (si no hay nada)
   - Muy raro, casi nunca ocurre

Esta columna permite hacer **JOIN** entre sesiones y clientes.

---

## 📈 Análisis ML (Opcional)

Si quieres hacer segmentación de clientes y análisis predictivo:

```bash
python analisis_ml.py
```

Este script genera:
- 4 segmentos de clientes
- Gráficos de perfiles por segmento
- Modelo predictivo de frecuencia de visitas
- Archivos en carpeta `output/`

---

## 🎯 Para Google Looker Studio

**Archivo a usar:** `DatosCompletos.csv`

Este archivo contiene:
- ✅ Todas las sesiones con sus tratamientos
- ✅ Datos de cada cliente vinculado por ID
- ✅ Fechas en formato ISO (`YYYY-MM-DD`)
- ✅ Columnas binarias (0/1) para filtros y agregaciones

---

## ⚙️ Configuración

### `main.py` (Procesamiento de Sesiones)
```python
umbral_frecuencia = 0.005       # Filtrar columnas que aparecen <0.5%
umbral_similitud = 85           # Fuzzy matching: 85% similitud
```

### Columnas Procesadas
- `tipo_tratamiento` - Tipos de tratamientos faciales
- `problemas_piel` - Acné, manchas, flacidez, etc.
- `zonas_tratadas` - Frente, ojeras, papada, etc.
- `productos` - Aceites, mascarillas, shots, etc.

---

## 🔧 Solución de Problemas

### Error: "No se encontró el archivo"
```bash
# Verifica que los archivos originales existan:
dir "Base - Sesiones.csv"
dir "Base - Clientes.csv"
```

### Error: "No hay columna ID"
```bash
# Ejecuta primero los scripts de procesamiento:
python main.py
python procesar_clientes.py
```

### Fechas no se ven bien en Looker
Las fechas ya están en formato ISO (`YYYY-MM-DD`). Si Looker no las reconoce:
1. En Looker: Editar campo → Tipo → Fecha
2. Formato: `YYYY-MM-DD`

---

## 📊 Estructura del Pipeline

```
Base - Sesiones.csv ──► main.py ──────────► SesionesFinal.csv ──┐
                                                                  │
                                                                  ├──► hacer_join.py ──► DatosCompletos.csv
                                                                  │
Base - Clientes.csv ──► procesar_clientes.py ──► ClientesFinal.csv ──┘
```

---

## 📝 Notas Importantes

1. **Orden de ejecución:** Siempre ejecutar `main.py` y `procesar_clientes.py` ANTES de `hacer_join.py`

2. **Consolidación fuzzy:** El script agrupa automáticamente términos similares:
   - "membresia", "membresía", "membresias" → `membresias`
   - "aceite", "aceite de jojoba", "aceite jojoba" → columnas separadas

3. **JOIN type:** Se usa LEFT JOIN desde sesiones, así no se pierden sesiones aunque no tengan datos de cliente

4. **Performance:** Con ~41k sesiones, el proceso toma 1-2 minutos

---

## 🎓 Preguntas Frecuentes

### ¿Por qué hay menos clientes únicos que sesiones?
Cada cliente puede tener múltiples sesiones. ~41k sesiones corresponden a ~8k clientes únicos.

### ¿Qué pasa si un ID de sesión no existe en clientes?
Se mantiene la sesión pero los campos de cliente quedarán vacíos (NULL). Esto es normal con LEFT JOIN.

### ¿Puedo modificar las columnas que se procesan?
Sí, edita la lista `columnas_a_procesar` en `main.py`.

---

**📧 Contacto:** Para dudas o problemas, consultar al equipo de análisis de SKINFIT.
