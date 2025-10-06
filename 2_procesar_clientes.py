import pandas as pd

# --- CONFIGURACIÓN ---
archivo_entrada = 'Base - Clientes.csv'
archivo_salida = 'ClientesFinal.csv'

print("="*70)
print("PROCESAMIENTO DE BASE - CLIENTES.CSV")
print("="*70)

# --- CARGA DE DATOS ---
try:
    df = pd.read_csv(archivo_entrada)
    print(f"\nArchivo '{archivo_entrada}' cargado. Dimensiones: {df.shape}")
    print(f"Columnas: {df.columns.tolist()}")
except FileNotFoundError:
    print(f"Error: No se pudo encontrar el archivo '{archivo_entrada}'.")
    exit()

# --- CREAR COLUMNA ID ---
def crear_id(row):
    """Crea un ID único usando email o nombre_apellido como fallback."""
    # Prioridad 1: Email
    email = row.get('Email') or row.get('email') or row.get('mail')
    if pd.notna(email) and str(email).strip() != '':
        return str(email).strip().lower()
    
    # Prioridad 2: Nombre + Apellido
    nombres = str(row.get('Nombres', '') or row.get('nombre', '')).strip()
    apellidos = str(row.get('Apellidos', '') or row.get('apellido', '')).strip()
    
    if nombres or apellidos:
        # Limpiar y combinar nombre_apellido
        id_nombre = f"{nombres}_{apellidos}".lower()
        id_nombre = id_nombre.replace(' ', '_')
        return id_nombre
    
    # Prioridad 3: Fallback con índice de fila
    return f"sin_id_{row.name}"

df['ID'] = df.apply(crear_id, axis=1)

# --- ESTADÍSTICAS ---
ids_con_email = df['ID'].str.contains('@', na=False).sum()
ids_con_nombre = (~df['ID'].str.contains('@', na=False) & ~df['ID'].str.contains('sin_id', na=False)).sum()
ids_sin_identificador = df['ID'].str.contains('sin_id', na=False).sum()

print(f"\nColumna 'ID' creada exitosamente:")
print(f"  - IDs con email: {ids_con_email} ({ids_con_email/len(df)*100:.1f}%)")
print(f"  - IDs con nombre_apellido: {ids_con_nombre} ({ids_con_nombre/len(df)*100:.1f}%)")
print(f"  - IDs sin identificador: {ids_sin_identificador} ({ids_sin_identificador/len(df)*100:.1f}%)")

# --- MOSTRAR EJEMPLOS ---
print("\nEjemplos de IDs creados:")
print(df[['Email', 'Nombres', 'Apellidos', 'ID']].head(10))

# --- GUARDAR RESULTADO ---
df.to_csv(archivo_salida, index=False, encoding='utf-8-sig')
print(f"\n¡Proceso completado! ✨")
print(f"Archivo guardado como: '{archivo_salida}'")
print(f"Dimensiones finales: {df.shape}")
print("="*70)
