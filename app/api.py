from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
import joblib
from typing import Dict, Any

app = FastAPI(
    title="Modelo de Predicción de Mora en Créditos",
    description="Una API para predecir la probabilidad de mora en créditos utilizando un modelo de machine learning entrenado con datos históricos.",
    version="1.0.0"
)

# RESOLUCIÓN DEL TODO
class PredictionRequest(BaseModel):
    # Se eliminó la llave anidada 'features: Dict...'. 
    # Ahora la API recibe los datos planos, exactamente como salieron del preprocesamiento.
    edad: int = Field(..., description="Edad del cliente.")
    antiguedad_empleado: float = Field(..., description="Antigüedad del empleado.")
    situacion_vivienda: str = Field(..., description="Situación de vivienda del cliente.")
    ingresos: int = Field(..., description="Ingresos del cliente.")
    objetivo_credito: str = Field(..., description="Objetivo del crédito.")
    pct_ingreso: float = Field(..., description="Porcentaje de ingreso destinado al crédito.")
    tasa_interes: float = Field(..., description="Tasa de interés del crédito.")
    estado_credito: int = Field(..., description="Estado del crédito.")
    antiguedad_cliente: float = Field(..., description="Antigüedad del cliente.")
    estado_civil: str = Field(..., description="Estado civil del cliente.")
    estado_cliente: str = Field(..., description="Estado del cliente.")
    genero: str = Field(..., description="Género del cliente.")
    limite_credito_tc: float = Field(..., description="Límite de crédito de tarjeta de crédito.")
    nivel_educativo: str = Field(..., description="Nivel educativo del cliente.")
    personas_a_cargo: float = Field(..., description="Número de personas a cargo del cliente.")
    capacidad_pago: float = Field(..., description="Capacidad de pago del cliente.")
    operaciones_mensuales: float = Field(..., description="Número de operaciones mensuales del cliente.")
    presion_financiera: float = Field(..., description="Presión financiera del cliente.")
    gasto_promedio_operacion: float = Field(..., description="Gasto promedio por operación del cliente.")
    operaciones_tarjeta_mensuales: float = Field(..., description="Número de operaciones mensuales con tarjeta del cliente.")
    estabilidad_laboral: float = Field(..., description="Estabilidad laboral del cliente.")

    class Config:
        json_schema_extra = {
            "example": {
                # El ejemplo se adaptó para reflejar el envío plano de variables
                "edad": 21,
                "antiguedad_empleado": 5.0,
                "situacion_vivienda": "PROPIA",
                "ingresos": 9600,
                "objetivo_credito": "EDUCACION",
                "pct_ingreso": 0.1,
                "tasa_interes": 11.14,
                "estado_credito": 0,
                "antiguedad_cliente": 39.0,
                "estado_civil": "CASADO",
                "estado_cliente": "ACTIVO",
                "genero": "M",
                "limite_credito_tc": 12691.0,
                "nivel_educativo": "SECUNDARIO_COMPLETO",
                "personas_a_cargo": 3.0,
                "capacidad_pago": 0.104167,
                "operaciones_mensuales": 3.5,
                "presion_financiera": 0.17125,
                "gasto_promedio_operacion": 27.238095,
                "operaciones_tarjeta_mensuales": 3.5,
                "estabilidad_laboral": 0.238095
            }
        }
    
class PredictionResponse(BaseModel):
    prediction: str
    probability: Dict[str, float]
    class_labels: Dict[str, str]
    model_info: Dict[str, str]

# Cargar el modelo entrenado
MODEL_PATH = "models/prod_model.pkl"

try:
    model = joblib.load(MODEL_PATH)
    print("Modelo cargado exitosamente.")
except FileNotFoundError:
    print(f"Error: No se encontró el modelo en la ruta {MODEL_PATH}. Asegúrate de que el modelo esté entrenado y guardado correctamente.")
    model = None
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    model = None

@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a la API de Predicción de Mora en Créditos.",
        "endpoints": {
            "/predict": "POST - Realiza una predicción de mora en créditos.",
            "/docs": "GET - Documentación interactiva de la API.",
            "/health": "GET - Verifica el estado de la API."
        }
    }

@app.get("/health")
def health_check():
    if model is not None:
        return {"status": "ok", "message": "La API está funcionando correctamente."}
    else:
        return {"status": "error", "message": "El modelo no está cargado. Verifica los logs para más detalles."}
    

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="El modelo no está disponible para realizar predicciones.")
    
    try:
        # Convertir las características a un DataFrame (ahora se mapea limpio y directo)
        input_data = pd.DataFrame([request.dict()])
        
        # Realizar la predicción
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0]
        
        # Mapear las etiquetas de clase a nombres legibles
        class_labels = model.named_steps['model'].classes_
        probability_dict = {
            str(class_labels[i]): float(probability[i]) for i in range(len(class_labels))
        }
        
        model_info = {
            "model_version": "1.0.0",
            "model_type": "Logistic Regression",
        }
        
        return PredictionResponse(
            prediction=str(prediction),
            probability=probability_dict,
            class_labels={
                "0": "No Mora",
                "1": "Mora"
            },
            model_info=model_info
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar la solicitud: {e}")