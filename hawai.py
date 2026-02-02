import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Control Losa Hawai - Gestión y Geotecnia", layout="wide")

# Encabezado profesional
st.title("🏗️ Control de Ejecución: Losa Entrepiso Nervada")
st.subheader("Proyecto: Club Hawai | Gestión y Geotecnia")

# --- ENTRADA DE DATOS ---
with st.sidebar:
    st.header("Parámetros de Obra")
    area = st.number_input("Área de la losa (m²)", min_value=1.0, value=100.0)
    st.info(f"Calculando para: {area} m²")

# --- CÁLCULOS TÉCNICOS ---
# Valores típicos para losa de 20cm
concreto = area * 0.11  # m3/m2 aprox
acero = area * 4.5      # kg/m2 aprox
bloques = area * 8      # unidades/m2

# --- DASHBOARD ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Concreto Estimado", f"{concreto:.2f} m³")
with col2:
    st.metric("Acero Requerido", f"{acero:.2f} kg")
with col3:
    st.metric("Bloques de Anime", f"{int(bloques)} und")

st.divider()

# --- BITÁCORA DE OBRA ---
st.header("📝 Generador de Bitácora (IA)")
etapa = st.selectbox("Seleccione etapa:", ["Encofrado", "Armado de Acero", "Vaciado", "Curado"])

if st.button("Generar Reporte para el Cliente"):
    # Texto corregido para Python
    reporte = f"Actúa como un Ingeniero Civil Residente experto. Redacta un asiento formal para el CUADERNO DE BITÁCORA para el proyecto Club Hawai, enfocándote en la etapa de {etapa}."
    st.success("Reporte listo para copiar:")
    st.write(reporte)

# Pie de página
st.markdown("---")
st.caption("© 2026 Gestión y Geotecnia - Control de Proyectos de Ingeniería")
