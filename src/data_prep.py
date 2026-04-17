# Se importan las librerías necesarias
import pandas as pd
# import numpy as np


def process_data (datos_creditos: str = "data/raw/datos_creditos.csv",
                    datos_tarjetas: str = "data/raw/datos_tarjetas.csv",
                    output_dir: str = "data/processed/") -> None:
    """Lee los datos de créditos y tarjetas, los integra, procesa las variables y guarda el resultado en un nuevo archivo CSV.

    Args:
        datos_credito (str): Ruta al archivo CSV de datos de créditos.
        datos_tarjetas (str): Ruta al archivo CSV de datos de tarjetas.
        output_dir (str): Directorio donde se guardará el archivo procesado.
    """

    df_creditos = pd.read_csv("data/raw/datos_creditos.csv", sep=";")
    df_tarjetas = pd.read_csv("data/raw/datos_tarjetas.csv", sep=";")

    ##################################################################################
    # Se filtran los datos para eliminar registros con edades superiores a 90 años
    ##################################################################################

    df_creditos_filtrado = df_creditos.copy()
    df_creditos_filtrado = df_creditos_filtrado[df_creditos_filtrado['edad'] < 90]

    ##################################################################################
    # Tratamiento de valores nulos para tasa_interes y antiguedad_empleado utilizando la mediana por grupo
    ##################################################################################

    df_creditos_filtrado['tasa_interes'] = df_creditos_filtrado.groupby("objetivo_credito")["tasa_interes"].transform(lambda x: x.fillna(x.median()))

    # Tratamiento de valores nulos para antiguedad_empleado
    df_creditos_filtrado['antiguedad_empleado'] = df_creditos_filtrado.groupby("edad")["antiguedad_empleado"].transform(lambda x: x.fillna(x.median()))

    ##################################################################################
    # Se integran los datos de créditos y tarjetas utilizando un merge
    ##################################################################################

    df_integrado = pd.merge(df_creditos_filtrado, df_tarjetas, on='id_cliente', how='inner')


    ##################################################################################
    # Se crean nuevos atributos a partir de las variables originales para enriquecer el dataset y facilitar el análisis posterior
    ##################################################################################
    
    # Capacidad de pago del cliente
    df_integrado["capacidad_pago"] = df_integrado["importe_solicitado"] / (df_integrado["ingresos"])
    # El número de operaciones mensuales del cliente
    df_integrado["operaciones_mensuales"] = df_integrado["operaciones_ult_12m"] / 12
    # Presión financiera del cliente (mensual)
    df_integrado["presion_financiera"] = (
        (df_integrado["gastos_ult_12m"] / 12 + df_integrado["importe_solicitado"] / (df_integrado["duracion_credito"] * 12)) / (df_integrado["ingresos"] / 12))
    # Gasto promedio por operación realizada por el cliente
    df_integrado["gasto_promedio_operacion"] = df_integrado["gastos_ult_12m"] / df_integrado["operaciones_ult_12m"]
    # Cantidad de operaciones mensuales con tarjeta de crédito
    df_integrado["operaciones_tarjeta_mensuales"] = df_integrado["operaciones_ult_12m"] / 12
    # Estabilidad laboral (antiguedad_empleado / edad)
    df_integrado["estabilidad_laboral"] = df_integrado["antiguedad_empleado"] / df_integrado["edad"]


    ##################################################################################
    # Se eliminan las columnas originales que ya no son necesarias para el análisis posterior, dejando solo las nuevas columnas procesadas
    ##################################################################################

    columnas_a_eliminar = [
    "id_cliente",
    "operaciones_ult_12m",
    "gastos_ult_12m",
    "importe_solicitado",
    "duracion_credito",
    "nivel_tarjeta"
    ]
    df_integrado.drop(columnas_a_eliminar, inplace=True, axis=1)

    ##################################################################################
    # Se exporta los datos procesados a un nuevo archivo CSV
    ##################################################################################
    df_integrado.to_csv(output_dir + "datos_integrados.csv", index=False)

if __name__ == "__main__":
    process_data()