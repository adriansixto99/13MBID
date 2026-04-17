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
    # Validación 1: Verificar que la edad esté entre 18 y 100 años
    edad_valida = df_creditos["edad"].between(18, 100).all()
    mensaje_edad = ""
    if not edad_valida:
        edades_fuera = df_creditos[(df_creditos["edad"] < 18) | (df_creditos["edad"] > 100)]["edad"].unique()
        mensaje_edad = f"Edades fuera de rango: {edades_fuera}"
    add_expectation(
        "rango_edad", #Verificar que la edad esté entre 18 y 100 años
        edad_valida,
        f"La edad debe estar entre 18 y 100 años. {mensaje_edad}"
    )

    # Validación 2: Rango de valores para situación de vivienda (ALQUILER, PROPIA, HIPOTECA, OTROS)
    vivienda_valida = df_creditos["situacion_vivienda"].isin(["ALQUILER", "PROPIA", "HIPOTECA", "OTROS"]).all()
    mensaje_vivienda = ""
    if not vivienda_valida:
        viviendas_fuera = df_creditos[~df_creditos["situacion_vivienda"].isin(["ALQUILER", "PROPIA", "HIPOTECA", "OTROS"])]["situacion_vivienda"].unique()
        mensaje_vivienda = f"Situaciones de vivienda inválidas: {viviendas_fuera}"    
    add_expectation(
        "situacion_vivienda", #Verificar que la situación de la vivienda sea válida
        vivienda_valida,
        f"La situación de la vivienda debe ser una de las opciones válidas. {mensaje_vivienda}"
    )

    # Validaciones para el dataset de tarjetas
    # Validación 1: Verificar que el límite de crédito sea mayor a 0
    tarjeta_limite_valida = (df_tarjetas["limite_credito_tc"] > 0).all()
    mensaje_limite = ""
    if not tarjeta_limite_valida:
        limites_invalidos = df_tarjetas[df_tarjetas["limite_credito_tc"] <= 0]["limite_credito_tc"].unique()
        mensaje_limite = f"Límites de crédito inválidos: {limites_invalidos}"
    add_expectation(
        "limite_credito_positivo",
        (df_tarjetas["limite_credito_tc"] > 0).all(),
        f"El límite de crédito de la tarjeta debe ser mayor a 0. {mensaje_limite}"
    )

    # Validación 2: Verificar que el nivel de tarjeta sea uno de los valores permitidos
    tarjeta_valor_valida = df_tarjetas["nivel_tarjeta"].isin(["Blue", "Silver", "Gold", "Platinum"]).all()
    mensaje_nivel = ""
    if not tarjeta_valor_valida:
        niveles_invalidos = df_tarjetas[~df_tarjetas["nivel_tarjeta"].isin(["Blue", "Silver", "Gold", "Platinum"])]["nivel_tarjeta"].unique()
        mensaje_nivel = f"Niveles de tarjeta inválidos: {niveles_invalidos}"        
    add_expectation(
        "nivel_tarjeta_valido",
        (df_tarjetas["nivel_tarjeta"].isin(["Blue", "Silver", "Gold", "Platinum"])).all(),
        f"El nivel de la tarjeta debe ser uno de los valores válidos (Blue, Silver, Gold, Platinum). {mensaje_nivel}"
    )

    
    # Resumen y validación final
    print("\n" + "="*70)
    print("RESUMEN DE VALIDACIONES")
    print("="*70)
    for exp in results["expectations"]:
        status = "✅ PASS" if exp["success"] else "❌ FAIL"
        print(f"{status}: {exp['expectation']}")
        if not exp["success"] and "message" in exp:
            print(f"   Detalles: {exp['message']}")
    print(f"\nTotal: {results['statistics']['success_count']}/{results['statistics']['total_count']}")
    print("="*70 + "\n")

    # Paso final: Hacer que el test falle si alguna expectativa no se cumplió
    assert results["success"], f"Se encontraron {results['statistics']['total_count'] - results['statistics']['success_count']} expectativas fallidas. Revisa el resumen para más detalles."