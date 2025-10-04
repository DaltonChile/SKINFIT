# -*- coding: utf-8 -*-
"""
ANALISIS ML Y SEGMENTACION DE CLIENTES PARA SKINFIT
----------------------------------------------------
Este script realiza segmentación y modelado predictivo usando los datos
YA consolidados y transformados por el script de preprocesamiento.

IMPORTANTE: Ejecutar primero main.py para generar el archivo transformado.
"""

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error

# --- CONFIGURACIÓN ---
config = {
    "input_filepath": "datos_finales_transformados_y_reducidos.csv",
    "output_dir": "output",
    "n_customer_clusters": 4,
    "test_size": 0.3,
    "random_state": 42
}

# --- FUNCIONES AUXILIARES ---

def save_plot(filename, title):
    """Guarda la figura actual en un archivo y la cierra."""
    if not os.path.exists(config["output_dir"]):
        os.makedirs(config["output_dir"])
    filepath = os.path.join(config["output_dir"], filename)
    plt.title(title, fontsize=14, weight="bold")
    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()
    print(f"Grafico guardado en: {filepath}")

# --- CARGA DE DATOS ---

def load_transformed_data(filepath):
    """Carga los datos ya transformados y consolidados."""
    print("Cargando datos transformados...")
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"No se encontro el archivo transformado: '{filepath}'.\n"
            "Por favor, ejecuta primero: python main.py"
        )
    
    df = pd.read_csv(filepath)
    print(f"Datos cargados: {df.shape[0]} filas x {df.shape[1]} columnas")
    return df

# --- AGREGACION A NIVEL DE CLIENTE ---

def aggregate_to_customer_level(df):
    """Agrega los datos de sesiones para crear un perfil por cliente."""
    print("\nAgregando datos a nivel de cliente...")
    
    # Identificar columnas que no deben agregarse
    exclude_cols = ['fecha', 'mail']
    
    # Identificar columnas numéricas (las one-hot encoded y otras)
    numeric_cols = [col for col in df.select_dtypes(include=["int64", "float64", "uint8", "int32", "int8"]).columns 
                    if col not in exclude_cols]
    
    print(f"Columnas numericas encontradas para agregacion: {len(numeric_cols)}")
    
    if 'mail' not in df.columns:
        raise ValueError("La columna 'mail' no existe en el DataFrame")
    
    # Agrupar por email y sumar (para contar ocurrencias)
    df_customers = df.groupby("mail")[numeric_cols].sum()
    
    # Contar número de sesiones
    df_customers["num_sesiones"] = df.groupby("mail").size()
    
    # Binarizar las características (1 si el cliente ha tenido esta característica al menos una vez)
    for col in numeric_cols:
        df_customers[col] = (df_customers[col] > 0).astype(int)
    
    df_customers.reset_index(inplace=True)
    print(f"Datos agregados: {len(df_customers)} clientes con {len(df_customers.columns)} columnas")
    
    return df_customers

# --- SEGMENTACION DE CLIENTES ---

def perform_customer_segmentation(df_customers, feature_cols):
    """Realiza clustering K-Means para segmentar a los clientes."""
    print("\nIniciando segmentacion de clientes...")
    X = df_customers[feature_cols].fillna(0)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    kmeans = KMeans(n_clusters=config["n_customer_clusters"], random_state=config["random_state"], n_init=10)
    df_customers["customer_segment"] = kmeans.fit_predict(X_scaled)
    
    # Visualización de perfiles
    segment_profiles = df_customers.groupby("customer_segment")[feature_cols].mean()
    
    # Seleccionar solo las top 50 características más variables para la visualización
    feature_variance = segment_profiles.var(axis=0).sort_values(ascending=False)
    top_features = feature_variance.head(50).index.tolist()
    
    plt.figure(figsize=(16, 12))
    sns.heatmap(segment_profiles[top_features].T, cmap="viridis", annot=True, fmt=".2f", cbar_kws={'label': 'Proporcion'})
    plt.xlabel('Segmento de Cliente', fontsize=12)
    plt.ylabel('Caracteristica', fontsize=12)
    save_plot("perfiles_segmentos_clientes.png", "Top 50 Caracteristicas por Segmento de Clientes")

    # Visualización PCA
    pca = PCA(n_components=2, random_state=config["random_state"])
    X_pca = pca.fit_transform(X_scaled)
    
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=df_customers["customer_segment"], 
                    palette="Set2", alpha=0.6, s=100, edgecolor='black', linewidth=0.5)
    plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} varianza)', fontsize=12)
    plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} varianza)', fontsize=12)
    plt.legend(title='Segmento', fontsize=10)
    save_plot("pca_segmentacion_clientes.png", "Visualizacion de Segmentos de Clientes (PCA)")
    
    print(f"Segmentacion de clientes finalizada. Se encontraron {config['n_customer_clusters']} segmentos.")
    
    # Mostrar estadísticas por segmento
    print("\nEstadisticas por segmento:")
    segment_stats = df_customers.groupby("customer_segment").agg({
        'num_sesiones': ['count', 'mean', 'std', 'min', 'max']
    }).round(2)
    print(segment_stats)
    
    return df_customers

# --- MODELO PREDICTIVO ---

def train_predictive_model(df_customers, feature_cols):
    """Entrena un modelo para predecir el número de sesiones."""
    print("\nIniciando entrenamiento del modelo predictivo...")
    X = df_customers[feature_cols]
    y = df_customers["num_sesiones"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config["test_size"], random_state=config["random_state"]
    )
    
    model = GradientBoostingRegressor(random_state=config["random_state"], n_estimators=100)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    r2 = r2_score(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    
    print(f"Modelo entrenado. R²: {r2:.3f}, RMSE: {rmse:.3f}")
    
    # Gráfico de importancia de variables (top 20)
    importances = pd.DataFrame({
        "feature": X.columns,
        "importance": model.feature_importances_
    }).sort_values("importance", ascending=False).head(20)
    
    plt.figure(figsize=(12, 8))
    sns.barplot(x="importance", y="feature", data=importances, palette="mako", hue="feature", legend=False)
    plt.xlabel('Importancia', fontsize=12)
    plt.ylabel('Caracteristica', fontsize=12)
    save_plot("importancia_variables_prediccion.png", "Top 20 Variables para Predecir Frecuencia de Visitas")
    
    # Scatter plot: predicciones vs reales
    plt.figure(figsize=(10, 8))
    plt.scatter(y_test, y_pred, alpha=0.5, edgecolor='black', linewidth=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Numero Real de Sesiones', fontsize=12)
    plt.ylabel('Numero Predicho de Sesiones', fontsize=12)
    plt.title(f'Predicciones vs Reales (R² = {r2:.3f})', fontsize=14, weight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(config["output_dir"], "predicciones_vs_reales.png"))
    plt.close()
    print(f"Grafico guardado en: {os.path.join(config['output_dir'], 'predicciones_vs_reales.png')}")
    
    return model

# --- EJECUCION PRINCIPAL ---

if __name__ == "__main__":
    print("="*70)
    print("ANALISIS ML Y SEGMENTACION DE CLIENTES - SKINFIT")
    print("="*70)
    
    # 1. Cargar datos transformados
    data = load_transformed_data(config["input_filepath"])
    
    # 2. Mostrar información sobre las columnas consolidadas
    print("\nColumnas en el dataset transformado:")
    print(f"  - Total: {len(data.columns)}")
    
    # Mostrar ejemplos de columnas consolidadas
    col_types = {}
    for col in data.columns:
        prefix = col.split('_')[0]
        col_types[prefix] = col_types.get(prefix, 0) + 1
    
    print("\nDistribucion de columnas por prefijo:")
    for prefix, count in sorted(col_types.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  - {prefix}: {count} columnas")
    
    # 3. Agregar a nivel de cliente
    df_customers = aggregate_to_customer_level(data)
    
    # 4. Preparar características para segmentación
    customer_feature_cols = [col for col in df_customers.columns 
                            if col not in ["mail", "num_sesiones"]]
    
    print(f"\nNumero de caracteristicas para segmentacion: {len(customer_feature_cols)}")
    
    # Verificar varianza
    if len(customer_feature_cols) == 0:
        raise ValueError("No hay columnas de características disponibles para la segmentación.")
    
    X_check = df_customers[customer_feature_cols].fillna(0)
    non_constant_cols = [col for col in customer_feature_cols if X_check[col].std() > 0]
    
    if len(non_constant_cols) < len(customer_feature_cols):
        print(f"Advertencia: {len(customer_feature_cols) - len(non_constant_cols)} columnas tienen varianza cero y seran excluidas")
        customer_feature_cols = non_constant_cols
    
    if len(customer_feature_cols) == 0:
        raise ValueError("Todas las columnas tienen varianza cero. No es posible realizar segmentacion.")
    
    print(f"Usando {len(customer_feature_cols)} caracteristicas para segmentacion")
    
    # 5. Segmentación de clientes
    df_segmented_customers = perform_customer_segmentation(df_customers, customer_feature_cols)
    
    # 6. Modelo predictivo
    model = train_predictive_model(df_segmented_customers, customer_feature_cols)
    
    # 7. Exportar resultados finales
    final_customer_filepath = os.path.join(config["output_dir"], "clientes_segmentados.csv")
    df_segmented_customers.to_csv(final_customer_filepath, index=False, encoding='utf-8-sig')
    print(f"\nReporte de clientes segmentados guardado en: {final_customer_filepath}")
    
    # 8. Resumen final
    print("\n" + "="*70)
    print("ANALISIS COMPLETADO CON EXITO")
    print("="*70)
    print(f"Total de clientes analizados: {len(df_segmented_customers)}")
    print(f"Total de sesiones: {df_segmented_customers['num_sesiones'].sum()}")
    print(f"Promedio de sesiones por cliente: {df_segmented_customers['num_sesiones'].mean():.2f}")
    print(f"Segmentos identificados: {config['n_customer_clusters']}")
    print("\nArchivos generados:")
    print(f"  - {final_customer_filepath}")
    print(f"  - {os.path.join(config['output_dir'], 'perfiles_segmentos_clientes.png')}")
    print(f"  - {os.path.join(config['output_dir'], 'pca_segmentacion_clientes.png')}")
    print(f"  - {os.path.join(config['output_dir'], 'importancia_variables_prediccion.png')}")
    print(f"  - {os.path.join(config['output_dir'], 'predicciones_vs_reales.png')}")
    print("="*70)
