"""
SCRIPT MAESTRO - SKINFIT
========================
Ejecuta todo el pipeline de procesamiento en orden correcto:
1. Procesa sesiones (main.py)
2. Procesa clientes (procesar_clientes.py)
3. Verifica compatibilidad (verificar_join.py)
4. Hace el JOIN (hacer_join.py)
"""

import subprocess
import sys

def ejecutar_script(nombre, descripcion):
    """Ejecuta un script de Python y maneja errores."""
    print("\n" + "="*70)
    print(f"▶️  {descripcion}")
    print("="*70)
    
    try:
        resultado = subprocess.run([sys.executable, nombre], check=True)
        print(f"✅ {nombre} completado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar {nombre}")
        print(f"   Código de error: {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo {nombre}")
        return False

# --- PIPELINE COMPLETO ---
print("🚀 INICIANDO PIPELINE COMPLETO - SKINFIT")
print("="*70)

pasos = [
    ("main.py", "PASO 1: Procesando sesiones (consolidación + transformación)"),
    ("procesar_clientes.py", "PASO 2: Procesando clientes (creación de ID)"),
    ("verificar_join.py", "PASO 3: Verificando compatibilidad de IDs"),
    ("hacer_join.py", "PASO 4: Haciendo JOIN de sesiones y clientes")
]

for i, (script, descripcion) in enumerate(pasos, 1):
    if not ejecutar_script(script, descripcion):
        print(f"\n❌ Pipeline detenido en el paso {i}")
        sys.exit(1)

# --- RESUMEN FINAL ---
print("\n" + "="*70)
print("🎉 PIPELINE COMPLETADO EXITOSAMENTE")
print("="*70)
print("\nArchivos generados:")
print("  📄 SesionesFinal.csv - Sesiones procesadas y consolidadas")
print("  📄 ClientesFinal.csv - Clientes con columna ID")
print("  📄 DatosCompletos.csv - JOIN completo (sesiones + clientes)")
print("\n✨ ¡Todo listo para usar en Google Looker Studio!")
print("="*70)
