import pandas as pd
from pandera.pandas import DataFrameSchema, Column, Check
import pytest

@pytest.fixture
def datos_creditos():
    """ Función para cargar los datos de créditos desde un archivo CSV.
    Returns:
        pd.DataFrame: DataFrame con los datos de créditos.
    """
    df = pd.read_csv("data/raw/datos_creditos.csv", sep=";")
    return df


@pytest.fixture
def datos_tarjetas():
    """ Función para cargar los datos de tarjetas desde un archivo CSV.
    Returns:
        pd.DataFrame: DataFrame con los datos de tarjetas.
    """
    df = pd.read_csv("data/raw/datos_tarjetas.csv", sep=";")
    return df


def test_esquema_datos_creditos(datos_creditos):
    """ Prueba para validar el esquema de los datos de créditos.
    Args:
        datos_creditos (pd.DataFrame): DataFrame con los datos de créditos.
    """
    esquema = DataFrameSchema({
        "id_cliente": Column(int, nullable=False),
        "edad": Column(int, Check.greater_than_or_equal_to(18)),
        "ingresos": Column(float, Check.greater_than_or_equal_to(0)),
        "falta_pago": Column(int, nullable=False)
    })
    esquema.validate(datos_creditos)