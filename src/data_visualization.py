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


if __name__ == "__main__":
    visualize_data()