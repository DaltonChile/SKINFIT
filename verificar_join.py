import pandas as pd

print("="*70)
print("VERIFICACIÓN DE COMPATIBILIDAD DE IDs PARA JOIN")
print("="*70)

# Cargar ambos archivos
df_clientes = pd.read_csv('ClientesFinal.csv')
df_sesiones = pd.read_csv('SesionesFinal.csv')

print(f"\n📊 ESTADÍSTICAS:")
print(f"  - Clientes: {len(df_clientes)} filas, {len(df_clientes['ID'].unique())} IDs únicos")
print(f"  - Sesiones: {len(df_sesiones)} filas, {len(df_sesiones['ID'].unique())} IDs únicos")

# Encontrar coincidencias
ids_clientes = set(df_clientes['ID'].str.lower().str.strip())
ids_sesiones = set(df_sesiones['ID'].str.lower().str.strip())

ids_en_ambos = ids_clientes.intersection(ids_sesiones)
ids_solo_clientes = ids_clientes - ids_sesiones
ids_solo_sesiones = ids_sesiones - ids_clientes

print(f"\n🔗 COMPATIBILIDAD PARA JOIN:")
print(f"  - IDs en ambos archivos: {len(ids_en_ambos)} ({len(ids_en_ambos)/len(ids_clientes)*100:.1f}% de clientes)")
print(f"  - IDs solo en clientes: {len(ids_solo_clientes)} ({len(ids_solo_clientes)/len(ids_clientes)*100:.1f}%)")
print(f"  - IDs solo en sesiones: {len(ids_solo_sesiones)} ({len(ids_solo_sesiones)/len(ids_sesiones)*100:.1f}%)")

# Verificar tipos de IDs que coinciden
ids_email_en_ambos = sum(1 for id in ids_en_ambos if '@' in id)
ids_nombre_en_ambos = len(ids_en_ambos) - ids_email_en_ambos

print(f"\n✉️ TIPOS DE IDs QUE COINCIDEN:")
print(f"  - Con email (@): {ids_email_en_ambos} ({ids_email_en_ambos/len(ids_en_ambos)*100:.1f}%)")
print(f"  - Con nombre_apellido: {ids_nombre_en_ambos} ({ids_nombre_en_ambos/len(ids_en_ambos)*100:.1f}%)")

# Ejemplo de JOIN
print(f"\n🔍 EJEMPLO DE JOIN:")
print(f"  SQL: SELECT * FROM clientes JOIN sesiones ON clientes.ID = sesiones.ID")
print(f"  Resultado: {len(ids_en_ambos)} clientes con sesiones vinculadas")

# Mostrar algunos ejemplos de IDs que coinciden
print(f"\n✅ EJEMPLOS DE IDs QUE COINCIDEN (primeros 10):")
for i, id_ejemplo in enumerate(list(ids_en_ambos)[:10], 1):
    sesiones_count = df_sesiones[df_sesiones['ID'].str.lower() == id_ejemplo].shape[0]
    print(f"  {i}. {id_ejemplo[:50]} - {sesiones_count} sesión(es)")

# Advertencia sobre IDs que no coinciden
if len(ids_solo_sesiones) > 0:
    print(f"\n⚠️ ADVERTENCIA: {len(ids_solo_sesiones)} IDs en sesiones no tienen perfil de cliente")
    print(f"   Estos registros quedarán huérfanos en un INNER JOIN")
    print(f"   Considera usar LEFT JOIN para mantener todas las sesiones")

print("\n" + "="*70)
print("✨ Los archivos están listos para hacer JOIN por la columna 'ID'")
print("="*70)
