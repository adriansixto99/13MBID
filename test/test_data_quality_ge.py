import pandas as pd
from pathlib import Path
import pytest
import warnings

warnings.filterwarnings(
    "ignore",
    message=".*Number.* field should not be instantiated.*",
)

import great_expectations as ge


pytestmark = [
    pytest.mark.filterwarnings("ignore:.*Number.* should not be instantiated.*"),
    pytest.mark.filterwarnings("ignore:.*result_format.*Validator.*el.*"),
    pytest.mark.filterwarnings("ignore:.*result_format.*Expectation.*level.*"),
]


# Paths
PROJECT_DIR = Path(".").resolve()
DATA_DIR = PROJECT_DIR / "data"


def test_great_expectations():
    """ Prueba para validar los datos de créditos utilizando Great Expectations.
    """
    # Cargar los datos de créditos y tarjetas
    df_creditos = pd.read_csv(DATA_DIR / "raw/datos_creditos.csv", sep=";")
    df_tarjetas = pd.read_csv(DATA_DIR / "raw/datos_tarjetas.csv", sep=";") 

    results = {
        "success": True,
        "expectations": [],
        "statistics": {"success_count": 0, "total_count": 0}
    }

    def add_expectation(expectation_name, condition, message=""):
        results["statistics"]["total_count"] += 1
        if condition:
            results["statistics"]["success_count"] += 1
            results["expectations"].append({
                "expectation": expectation_name,
                "success": True
            })
        else:
            results["success"] = False
            results["expectations"].append({
                "expectation": expectation_name,
                "success": False,
                "message": message
            })
    # Atributo a analizar: Exactitud (rangos de valores en datos)
    add_expectation(
        "rango_edad", #Verificar que la edad esté entre 18 y 100 años
        df_creditos["edad"].between(18, 100).all(), # La validación a realizar
        "La edad debe estar entre 18 y 100 años." # Mensaje de error en caso de que la validación falle
    )
    add_expectation(
        "situacion_vivienda", #Verificar que la situación de la vivienda sea válida
        (df_creditos["situacion_vivienda"].isin(["ALQUILER", "PROPIA", "HIPOTECA", "OTROS"])).all(),
        "La situación de la vivienda debe ser una de las opciones válidas."
    )



#############################################
#TODO: Agregar al menos (2) dos validaciones más para el dataser de tarjetas.
# Por ejemplo: rangos de valores para el atributo de límite de crédito o el tipo de tarjeta.
##############################################

