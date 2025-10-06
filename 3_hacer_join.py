"""
Script para hacer JOIN entre sesiones y clientes usando la columna ID
"""
import pandas as pd

print("="*70)
print("JOIN DE SESIONES Y CLIENTES - SKINFIT")
print("="*70)

# 1. Cargar archivos
print("\n1. Cargando archivos...")
try:
    df_sesiones = pd.read_csv('SesionesFinal.csv')
    print(f"   ✓ Sesiones cargadas: {df_sesiones.shape[0]:,} filas x {df_sesiones.shape[1]} columnas")
except FileNotFoundError:
    print("   ✗ ERROR: No se encontró 'SesionesFinal.csv'")
    print("   Por favor, ejecuta primero: python main.py")
    exit(1)

try:
    df_clientes = pd.read_csv('ClientesFinal.csv')
    print(f"   ✓ Clientes cargados: {df_clientes.shape[0]:,} filas x {df_clientes.shape[1]} columnas")
    
    # ELIMINAR DUPLICADOS: Mantener solo el primer registro por ID
    clientes_antes = len(df_clientes)
    df_clientes = df_clientes.drop_duplicates(subset=['ID'], keep='first')
    clientes_despues = len(df_clientes)
    duplicados_eliminados = clientes_antes - clientes_despues
    
    if duplicados_eliminados > 0:
        print(f"   ℹ️  Duplicados eliminados: {duplicados_eliminados:,} filas (manteniendo primera aparición)")
    
except FileNotFoundError:
    print("   ✗ ERROR: No se encontró 'ClientesFinal.csv'")
    print("   Por favor, ejecuta primero: python procesar_clientes.py")
    exit(1)

# 2. Verificar que ambos tengan columna ID
print("\n2. Verificando columna ID...")
if 'ID' not in df_sesiones.columns:
    print("   ✗ ERROR: No hay columna 'ID' en sesiones")
    exit(1)
if 'ID' not in df_clientes.columns:
    print("   ✗ ERROR: No hay columna 'ID' en clientes")
    exit(1)

print(f"   ✓ IDs únicos en sesiones: {df_sesiones['ID'].nunique():,}")
print(f"   ✓ IDs únicos en clientes: {df_clientes['ID'].nunique():,}")

# 3. Verificar coincidencias
ids_sesiones = set(df_sesiones['ID'].unique())
ids_clientes = set(df_clientes['ID'].unique())
ids_comunes = ids_sesiones.intersection(ids_clientes)
ids_solo_sesiones = ids_sesiones - ids_clientes
ids_solo_clientes = ids_clientes - ids_sesiones

print(f"\n3. Análisis de coincidencias:")
print(f"   • IDs en ambos archivos: {len(ids_comunes):,} ({len(ids_comunes)/len(ids_sesiones)*100:.1f}%)")
print(f"   • IDs solo en sesiones: {len(ids_solo_sesiones):,}")
print(f"   • IDs solo en clientes: {len(ids_solo_clientes):,}")

if len(ids_solo_sesiones) > 0:
    print(f"\n   ⚠️  Advertencia: {len(ids_solo_sesiones)} IDs de sesiones no tienen datos de cliente")
    print(f"      Ejemplos: {list(ids_solo_sesiones)[:5]}")

# 4. Hacer el JOIN (OUTER JOIN para incluir todos los clientes)
print(f"\n4. Realizando JOIN (OUTER JOIN - incluye todos los clientes)...")

# OPTIMIZACIÓN: Solo incluir columnas esenciales de clientes para reducir tamaño
columnas_esenciales_clientes = ['ID']

# Buscar columnas de nombre, apellido y mail (pueden tener diferentes nombres)
for col in df_clientes.columns:
    col_lower = col.lower()
    if col_lower in ['nombre', 'nombres', 'apellido', 'apellidos', 'mail', 'email']:
        columnas_esenciales_clientes.append(col)

# Filtrar solo columnas que existen
columnas_esenciales_clientes = [col for col in columnas_esenciales_clientes if col in df_clientes.columns]
df_clientes_reducido = df_clientes[columnas_esenciales_clientes].copy()

print(f"   ℹ️  Columnas de clientes incluidas: {[col for col in columnas_esenciales_clientes if col != 'ID']}")

# Hacer el OUTER JOIN para incluir todos los clientes (con y sin sesiones)
df_join = df_sesiones.merge(df_clientes_reducido, on='ID', how='outer', suffixes=('_sesion', '_cliente'))

print(f"   ℹ️  Columna 'ID' mantenida para facilitar conteo de clientes únicos")
print(f"   ✓ JOIN completado: {df_join.shape[0]:,} filas x {df_join.shape[1]} columnas")

# Contar clientes sin sesiones
clientes_sin_sesiones = df_join[df_join['fecha'].isna()].shape[0] if 'fecha' in df_join.columns else 0
print(f"   ℹ️  Clientes sin sesiones incluidos: {clientes_sin_sesiones:,}")

# 5. Verificar resultados
print(f"\n5. Verificación del JOIN:")
# Buscar una columna de clientes para verificar
cols_cliente_verificar = [col for col in df_join.columns if col.lower() in ['nombre', 'nombres', 'mail', 'email']]
if cols_cliente_verificar:
    filas_sin_datos_cliente = df_join[cols_cliente_verificar[0]].isna().sum()
    if filas_sin_datos_cliente > 0:
        print(f"   ⚠️  {filas_sin_datos_cliente:,} sesiones no tienen datos de cliente asociados")
    else:
        print(f"   ✓ Todas las sesiones tienen datos de cliente")
else:
    print(f"   ℹ️  No se pudo verificar datos de cliente")

# 6. Guardar resultado
archivo_salida = 'DatosCompletos.csv'
df_join.to_csv(archivo_salida, index=False, encoding='utf-8-sig')
print(f"\n6. Archivo guardado: '{archivo_salida}'")

# 7. Resumen de columnas
print(f"\n7. Resumen de columnas en el archivo final:")
print(f"   • Total de columnas: {len(df_join.columns)}")

# Agrupar columnas por prefijo
prefijos = {}
for col in df_join.columns:
    if col == 'ID':
        continue
    prefijo = col.split('_')[0]
    prefijos[prefijo] = prefijos.get(prefijo, 0) + 1

print(f"\n   Columnas por categoría (top 10):")
for prefijo, count in sorted(prefijos.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"      - {prefijo}: {count} columnas")

print("\n" + "="*70)
print("✨ JOIN COMPLETADO EXITOSAMENTE")
print("="*70)
print(f"\nArchivo de salida: {archivo_salida}")
print(f"Filas totales: {df_join.shape[0]:,}")
print(f"Columnas: {df_join.shape[1]}")
print(f"\nClientes únicos totales: {df_join['ID'].nunique():,}")
print(f"  • Con sesiones: {len(ids_comunes):,}")
print(f"  • Sin sesiones: {len(ids_solo_clientes):,}")
print("\n✅ Incluye TODOS los clientes (con y sin sesiones)")
print("✅ Listo para usar en Google Looker Studio!")
