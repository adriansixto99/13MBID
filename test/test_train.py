from src.train_model import train_model
import json
from pathlib import Path
import pytest

def test_train_model(tmp_path):
    # Se tiene que establecer la raíz del proyecto para acceder a los archivos de datos y métricas de referencia
    project_root = Path(__file__).resolve().parents[1]

    baseline_path = project_root / "metrics" / "train_metrics.json"
    if not baseline_path.exists():
        pytest.skip("Baseline metrics not found. Run train_model.py to generate reference metrics.")
    
    with open(baseline_path, "r") as f:
        baseline = json.load(f)

    #Ejecutar el entrenamiento
    data_path = project_root / "data" / "processed" / "datos_integrados.csv"
    model_output = tmp_path / "prod_model.pkl"
    preprocessor_output = tmp_path / "prod_preprocessor.pkl"
    metrics_output = tmp_path / "train_metrics.json"

    # El entrenamiento debería generar un archivo de métricas JSON junto con el modelo y el preprocesador
    _, _, metrics = train_model(
        data_path=str(data_path),
        model_path=str(model_output),
        preprocessor_path=str(preprocessor_output),
        metrics_path=str(metrics_output)
    )

    assert set(metrics.keys()) == set(baseline.keys()), "Las métricas generadas no coinciden con las métricas de referencia."

    atol = 1e-9
    for k in baseline.keys():
        assert metrics[k] == pytest.approx(baseline[k], rel=0, abs=atol)
        (f"Métrica '{k}' cambió: baseline={baseline[k]} nueva={metrics[k]}"
        )

    
if __name__ == "__main__":
    test_train_model()


