# Importación de librerías y supresión de advertencias
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def visualize_data(datos_creditos: str = "data/raw/datos_creditos.csv",
                    datos_tarjetas: str = "data/raw/datos_tarjetas.csv",
                    output_dir: str = "docs/figures/") -> None:
    """
    Generar visualizaciones de los datos del escenario
    mediante gráficos de Seaborn y Matplotlib.

    Args:
        datos_creditos (str): Ruta al archivo CSV de datos de créditos.
        datos_tarjetas (str): Ruta al archivo CSV de datos de tarjetas.
        output_dir (str): Directorio donde se guardarán las figuras generadas.

    Returns:
        None
    """
    # Crear el directorio de salida si no existe
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Lectura de los datos
    df_creditos = pd.read_csv(datos_creditos, sep=";")
    df_tarjetas = pd.read_csv(datos_tarjetas, sep=";")

    
    sns.set_style("whitegrid")

    # Gráfico de distribución de la variable 'target'
    plt.figure(figsize=(10, 6))
    sns.countplot(x='falta_pago', data=df_creditos)
    plt.title('Distribución de la variable target')
    plt.xlabel('¿Presentó mora el cliente?')
    plt.ylabel('Cantidad de clientes')
    plt.savefig(output_dir / 'target_distribution.png')
    plt.close()

    # Gráfico de correlación entre variables numéricas
    num_df = df_creditos.select_dtypes(include=['float64', 'int64'])
    corr = num_df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Matriz de correlaciones - Créditos')
    plt.savefig(output_dir / 'correlation_heatmap_creditos.png')
    plt.close()

    # Gráfico de correlación entre variables numéricas
    num_df = df_tarjetas.select_dtypes(include=['float64', 'int64'])
    corr = num_df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Matriz de correlaciones - Tarjetas')
    plt.savefig(output_dir / 'correlation_heatmap_tarjetas.png')
    plt.close()

    ##################################################################################s
    # TODO: Agregar al menos dos (2) gráficos adicionales que consideren variables.
    # OPCIÓN EXTRA (ejemplo):  agregar la generación del reporte con ydata-profiling.
    ##################################################################################
    
    # 1. Gráfico de dispersión: Relación entre Ingresos, Importe Solicitado y Mora (Créditos)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='ingresos', y='importe_solicitado', hue='falta_pago', 
                    data=df_creditos, alpha=0.6, palette='coolwarm')
    plt.title('Relación entre Ingresos y Monto Solicitado según estado de Mora')
    plt.xlabel('Ingresos Anuales')
    plt.ylabel('Importe Solicitado')
    plt.savefig(output_dir / 'scatter_ingresos_importe.png', bbox_inches='tight')
    plt.close()

    # 2. Gráfico de cajas: Límite de Crédito según el Nivel de Tarjeta (Tarjetas)
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='nivel_tarjeta', y='limite_credito_tc', data=df_tarjetas, palette='Set3')
    plt.title('Distribución del Límite de Crédito por Nivel de Tarjeta')
    plt.xlabel('Nivel de Tarjeta')
    plt.ylabel('Límite de Crédito')
    plt.savefig(output_dir / 'boxplot_limite_nivel.png', bbox_inches='tight')
    plt.close()

    # 3. Gráfico de barras: Mora por objetivo del crédito (Créditos)
    plt.figure(figsize=(12, 6))
    sns.countplot(x='objetivo_credito', hue='falta_pago', data=df_creditos, palette='viridis')
    plt.title('Estado de Mora según el Objetivo del Crédito')
    plt.xlabel('Objetivo del Crédito')
    plt.ylabel('Cantidad de Clientes')
    plt.xticks(rotation=45, ha='right') # Rotamos las etiquetas para mejor legibilidad
    plt.savefig(output_dir / 'countplot_objetivo_mora.png', bbox_inches='tight')
    plt.close()

    ##################################################################################
    # OPCIÓN EXTRA: agregar la generación del reporte con ydata-profiling.
    ##################################################################################
    try:
        from ydata_profiling import ProfileReport
        
        print("Generando reportes de ydata-profiling (esto puede tomar unos segundos)...")
        # Reporte de créditos
        profile_creditos = ProfileReport(df_creditos, title="Reporte de Profiling - Créditos")
        profile_creditos.to_file(output_dir / "reporte_creditos.html")
        
        # Reporte de tarjetas
        profile_tarjetas = ProfileReport(df_tarjetas, title="Reporte de Profiling - Tarjetas")
        profile_tarjetas.to_file(output_dir / "reporte_tarjetas.html")
        print("¡Reportes HTML generados con éxito!")
        
    except ImportError:
        print("Aviso: 'ydata-profiling' no está instalada. Ejecuta 'pip install ydata-profiling' si deseas los reportes.")

if __name__ == "__main__":
    visualize_data()