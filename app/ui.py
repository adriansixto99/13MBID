import streamlit as st
import requests

st.set_page_config(
    page_title="Predicción de Mora en Créditos", 
    page_icon=":credit_card:", 
    layout="wide"
)

with st.sidebar:
    st.header("Instrucciones")
    st.write("""
    1. Ingrese los detalles del crédito en el formulario.
    2. Haga clic en el botón "Predecir" para obtener la probabilidad de mora.
    3. Interprete los resultados para tomar decisiones informadas.
    """)
    st.header("Configuración de la API")
    api_url = st.text_input(
        "URL de la API", 
        value="http://localhost:8000",
        help="Ingrese la URL donde se encuentra desplegada la API de predicción."
    )
    st.divider()
    if st.button("Probar Conexión a la API"):
        try:
            response = requests.get(f"{api_url}/health", timeout=5)
            if response.status_code == 200:
                st.success("Conexión exitosa a la API.")
            else:
                st.error("La API respondió, pero con un error.")
        except Exception as e:
            st.error(f"No se pudo conectar a la API: {e}")

st.title("Predicción de Mora en Créditos")
st.write("Ingrese los detalles del crédito para obtener un análisis de riesgo en tiempo real.")

with st.form("prediction_form"):
    st.subheader("1. Datos Personales")
    col1, col2, col3 = st.columns(3)

    with col1:
        edad = st.number_input("Edad", min_value=18, max_value=100, value=30)
        genero = st.selectbox("Género", options=["M", "F"])
        estado_civil = st.selectbox("Estado Civil", options=["SOLTERO", "CASADO", "DIVORCIADO", "VIUDO", "OTRO"])

    with col2:
        nivel_educativo = st.selectbox(
            "Nivel Educativo",
            options=["PRIMARIO", "SECUNDARIO", "TERCIARIO", "UNIVERSITARIO_INCOMPLETO","UNIVERSITARIO_COMPLETO"])
        situacion_vivienda = st.selectbox(
            "Situación de Vivienda",
            options=["ALQUILER", "PROPIETARIO", "HIPOTECADA", "OTRA"])
        personas_a_cargo = st.number_input("Personas a Cargo", min_value=0.0, max_value=20.0, value=0.0)

    with col3:
        estado_cliente = st.selectbox("Estado del Cliente", options=["ACTIVO", "INACTIVO"])
        antiguedad_cliente = st.number_input("Antigüedad como cliente (meses)", min_value=0.0, value=12.0)

    st.divider()
    st.subheader("2. Información Financiera y del Crédito")
    col4, col5, col6 = st.columns(3)

    with col4:
        ingresos = st.number_input("Ingresos mensuales (€)", min_value=1, value=50000)
        antiguedad_empleado = st.number_input("Antigüedad laboral (años)", min_value=0.0, max_value=50.0, value=2.0)

    with col5:
        objetivo_credito = st.selectbox(
            "Objetivo del crédito",
            options=["PERSONAL","VIVIENDA","VEHICULO","NEGOCIOS", "EDUCACION","OTRO"]
        )
        importe_solicitado = st.number_input("Importe solicitado (€)", min_value=1, value=15000)
        duracion_credito = st.number_input("Plazo del crédito (años)", min_value=1, max_value=30, value=5)

    with col6:
        tasa_interes = st.number_input("Tasa de interés (%)", min_value=0.0, max_value=100.0, value=10.0)
        estado_credito = st.number_input("Estado del Crédito (0=Al día, 1=Mora)", min_value=0, max_value=1, step=1)
        pct_ingreso = st.number_input("Porcentaje de Ingreso destinado al pago (0.0 a 1.0)", min_value=0.0, max_value=1.0, value=0.1)

    st.divider()
    st.subheader("3. Gastos y Comportamiento con Tarjetas")
    col7, col8 = st.columns(2)

    with col7:
        limite_credito_tc = st.number_input("Límite de crédito en Tarjeta (€)", min_value=0.0, value=10000.0)

    with col8:
        gastos_ult_12m = st.number_input("Gastos totales último año (€)", min_value=0.0, value=5000.0)
        operaciones_ult_12m = st.number_input("Nro. de operaciones realizadas en el año", min_value=1.0, value=60.0)
    
    st.divider()
    submit_button = st.form_submit_button(
        "Predecir Riesgo de Mora",
        use_container_width=True,
        type="primary"
    )

# --- RESOLUCIÓN DEL TODO ---
if submit_button:
    # 1. Cálculos de Ingeniería de Características 
    ingresos_anuales = ingresos * 12
    ingresos_mensuales_seguros = max(ingresos, 1) # Evitar división por cero
    
    # Capacidad de pago: Importe pedido / Ingresos anuales
    calc_capacidad_pago = importe_solicitado / max(ingresos_anuales, 1)
    
    # Operaciones mensuales: Total anual / 12
    calc_operaciones_mensuales = operaciones_ult_12m / 12
    
    # Presión financiera: (Gastos mensuales + Cuota préstamo) / Ingresos mensuales
    gastos_mensuales = gastos_ult_12m / 12
    cuota_estimada = importe_solicitado / (duracion_credito * 12)
    calc_presion_financiera = (gastos_mensuales + cuota_estimada) / ingresos_mensuales_seguros
    
    # Gasto promedio por operación
    calc_gasto_promedio = gastos_ult_12m / max(operaciones_ult_12m, 1)
    
    # Estabilidad laboral: Años trabajando / Edad
    calc_estabilidad_laboral = antiguedad_empleado / max(edad, 1)

    # 2. Construcción del diccionario para la API
    data_dict = {
        "edad": int(edad),
        "antiguedad_empleado": float(antiguedad_empleado),
        "situacion_vivienda": situacion_vivienda,
        "ingresos": int(ingresos),
        "objetivo_credito": objetivo_credito,
        "pct_ingreso": float(pct_ingreso),
        "tasa_interes": float(tasa_interes),
        "estado_credito": int(estado_credito),
        "antiguedad_cliente": float(antiguedad_cliente),
        "estado_civil": estado_civil,
        "estado_cliente": estado_cliente,
        "genero": genero,
        "limite_credito_tc": float(limite_credito_tc),
        "nivel_educativo": nivel_educativo,
        "personas_a_cargo": float(personas_a_cargo),
        "capacidad_pago": float(calc_capacidad_pago),
        "operaciones_mensuales": float(calc_operaciones_mensuales),
        "presion_financiera": float(calc_presion_financiera),
        "gasto_promedio_operacion": float(calc_gasto_promedio),
        "operaciones_tarjeta_mensuales": float(calc_operaciones_mensuales), 
        "estabilidad_laboral": float(calc_estabilidad_laboral),
        "gastos_ult_12m": float(gastos_ult_12m)
    }

    # Payload compatible con PredictionRequest
    payload = {
        "features": data_dict,
        **data_dict
    }

    try:
        response = requests.post(f"{api_url}/predict", json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()

        st.divider()
        st.subheader("📊 Resultado de la Predicción")

        prediction = result["prediction"]
        prob = result.get("probability", {})
        labels = result.get("class_labels", {"0": "No entra en mora", "1": "Entra en mora"})
        label_text = labels.get(str(prediction), prediction)

        col_res1, col_res2 = st.columns(2)

        with col_res1:
            if str(prediction) == "1":
                st.error(f"### **Predicción: {label_text}**")
            else:
                st.success(f"### **Predicción: {label_text}**")

        with col_res2:
            prob_mora = prob.get("1", 0)
            prob_no_mora = prob.get("0", 1 - prob_mora)
            st.metric("Riesgo de Mora", f"{prob_mora * 100:.2f}%")
            st.metric("Seguridad de Pago", f"{prob_no_mora * 100:.2f}%")

        with st.expander("Detalles técnicos de la respuesta (API JSON)"):
            st.json(result)

    except requests.exceptions.HTTPError as e:
        st.error(f"Error de validación (422): Asegúrate de que api.py use 'Any' en la clase PredictionRequest.")
        st.info(f"Detalle del error: {response.json()}")
    except Exception as e:
        st.error(f"No se pudo completar la predicción: {e}")