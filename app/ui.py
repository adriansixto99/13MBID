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
st.write("Ingrese los detalles del crédito para predecir la probabilidad de mora.")

with st.form("prediction_form"):
    st.subheader("Datos del cliente")
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
        estado_credito = st.number_input("Estado del Crédito", min_value=0, max_value=1, step=1)

    st.divider()
    st.subheader("Información financiera y laboral")
    col4, col5, col6 = st.columns(3)

    with col4:
        ingresos = st.number_input("Ingresos", min_value=0, value=50000)
        antiguedad_empleado = st.number_input("Antigüedad en el empleo (años)", min_value=0.0, max_value=50.0, value=1.0)

    with col5:
        objetivo_credito = st.selectbox(
            "Objetivo del crédito",
            options=["PERSONAL","VIVIENDA","VEHICULO","NEGOCIOS", "EDUCACION","OTRO"]
        )
        tasa_interes = st.number_input("Tasa de interés (%)", min_value=0.0, max_value=100.0, value=10.0)
        pct_ingreso = st.number_input("Porcentaje de Ingreso(%)", min_value=0.0, max_value=1.0, value=0.1)

    with col6:
        capacidad_pago = st.number_input("Capacidad de pago", min_value=0.0, value=0.50, step=0.01, format="%.4f")
        presion_financiera = st.number_input("Presión financiera", min_value=0.0, value=2.0, step=0.01, format="%.4f")
        antiguedad_cliente = st.number_input("Antigüedad cliente (meses)", min_value=0.0, value=1.0)

    st.divider()
    st.subheader("Gastos y Límites")
    col7, col8 = st.columns(2)

    with col7:
        limite_credito_tc = st.number_input("Límite de crédito tarjeta de crédito", min_value=0.0, value=10000.0, step=100.0)

    with col8:
        gastos_ult_12m = st.number_input("Gastos último año", min_value=0.0, value=50.0, step=0.01, format="%.4f")
        operaciones_mensuales = st.number_input("Operaciones mensuales", min_value=0.0, value=5.0, step=1.0)
    
    st.divider()
    submit_button = st.form_submit_button(
        "Predecir",
        use_container_width=True,
        type="primary"
    )

if submit_button:
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
        "capacidad_pago": float(capacidad_pago),
        "operaciones_mensuales": float(operaciones_mensuales),
        "presion_financiera": float(presion_financiera),
        "gasto_promedio_operacion": 0.0,
        "operaciones_tarjeta_mensuales": 0.0,
        "estabilidad_laboral": 0.0
    }

    payload = {
        "features": data_dict, 
        **data_dict           
    }

    try:
        resp = requests.post(f"{api_url}/predict", json=payload, timeout=10)
        resp.raise_for_status()
        result = resp.json()

        st.divider()
        st.subheader("📊 Resultado de la predicción")

        prediction = result["prediction"]
        prob = result.get("probability", {})
        labels = result.get("class_labels", {"0": "No entra en mora", "1": "Entra en mora"})

        label_text = labels.get(str(prediction), prediction)

        col_res1, col_res2 = st.columns(2)

        with col_res1:
            if str(prediction) == "1":
                st.error(f"**Predicción: {label_text}**")
            else:
                st.success(f"**Predicción: {label_text}**")

        with col_res2:
            prob_mora = prob.get("1", prob.get(str(prediction), 0))
            prob_no_mora = prob.get("0", 1 - prob_mora)
            st.metric("Probabilidad de mora", f"{prob_mora * 100:.1f}%")
            st.metric("Probabilidad de no mora", f"{prob_no_mora * 100:.1f}%")

        with st.expander("Ver respuesta completa de la API"):
            st.json(result)

    except requests.exceptions.ConnectionError:
        st.error("No se pudo conectar con la API. Verificá la URL en el panel lateral.")
    except requests.exceptions.HTTPError as e:
        st.error(f"Error de la API ({resp.status_code}): {resp.json().get('detail')}")
    except Exception as e:
        st.error(f"Error inesperado: {e}")