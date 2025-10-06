"""
🚀 SKINFIT - EJECUTAR TODO
===========================
Este script ejecuta todo el pipeline automáticamente.

Simplemente ejecuta: python RUN.py

El proceso completo genera el archivo DatosCompletos.csv
listo para usar en Google Looker Studio.
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
    ("1_procesar_sesiones.py", "PASO 1: Procesando sesiones (consolidación + binarización)"),
    ("2_procesar_clientes.py", "PASO 2: Procesando clientes (creación de ID)"),
    ("3_hacer_join.py", "PASO 3: Haciendo JOIN (sesiones + clientes)")
]

for i, (script, descripcion) in enumerate(pasos, 1):
    if not ejecutar_script(script, descripcion):
        print(f"\n❌ Pipeline detenido en el paso {i}")
        sys.exit(1)

# --- RESUMEN FINAL ---
print("\n" + "="*70)
print("🎉 PIPELINE COMPLETADO EXITOSAMENTE")
print("="*70)
print("\n📁 Archivo generado:")
print("  ✅ DatosCompletos.csv - Archivo final para Google Looker")
print("\n� Contiene:")
print("  • Todas las sesiones con datos procesados")
print("  • Todos los clientes (con y sin sesiones)")
print("  • Columnas binarizadas listas para análisis")
print("\n✨ ¡Listo para usar en Google Looker Studio!")
print("="*70)
