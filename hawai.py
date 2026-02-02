import streamlit as st
import pandas as pd
import requests

# Configuración de la interfaz (Estilo React)
st.set_page_config(page_title="HM RENDERING - Club Hawai", layout="wide")

# Estilo personalizado para imitar el look de React/Tailwind
st.markdown("""
    <style>
    .hexagon-mask {
        background-color: black;
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        text-align: center;
    }
    .kpi-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid black;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER / BRANDING ---
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.markdown('<div class="hexagon-mask text-xl">HM</div>', unsafe_allow_html=True)
with col_title:
    st.markdown("### HM RENDERING STUDIO 3D")
    st.caption("PROYECTO: CLUB HAWAI | Ejecución de Losa Entrepiso")

st.divider()

# --- KPI CARDS (Métricas principales) ---
area_total = 265
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Área Total", f"{area_total} m²")
with c2:
    st.metric("Tiempo Estimado", "~17 Días")
with c3:
    st.metric("Concreto", "210 kg/cm²")
with c4:
    st.metric("Espesor Losa", "20 cm")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📅 Cronograma", "📦 Materiales", "✨ Asistente IA"])

with tab1:
    st.subheader("Ruta de Ejecución")
    actividades = [
        {"act": "Encofrado y Apuntalamiento", "dur": "5 Días", "desc": "Nivelación y parales."},
        {"act": "Armado de Bloques y Acero", "dur": "4 Días", "desc": "Anime y malla electrosoldada."},
        {"act": "Vaciado de Concreto", "dur": "1 Día", "desc": "Vaciado monolítico f'c 210."},
        {"act": "Curado de Concreto", "dur": "7 Días", "desc": "Riego continuo."}
    ]
    for a in actividades:
        with st.expander(f"{a['act']} - {a['dur']}"):
            st.write(a['desc'])
            st.progress(20)

with tab2:
    st.subheader("Inventario de Materiales")
    opcion = st.radio("Selecciona opción de refuerzo:", ["Opción A: Cabilla", "Opción B: Cercha"])
    
    # Datos de materiales
    mat_data = {
        "Material": ["Cemento Gris", "Piedra Picada", "Arena Lavada", "Bloque Anime", "Malla Electrosoldada"],
        "Cantidad": ["159 Sacos", "19 m³", "8 m³", "175 Pzas", "4 Rollos"]
    }
    st.table(pd.DataFrame(mat_data))
    
    if opcion == "Opción A: Cabilla":
        st.info("Refuerzo: 116 Piezas de Varilla 3/8\" (L=6m)")
    else:
        st.info("Refuerzo: 58 Piezas de Cercha 15cm (L=6m)")

with tab3:
    st.subheader("Generador de Bitácora con IA")
    notas = st.text_area("Escribe lo ocurrido hoy en la obra:")
    
    if st.button("Generar Reporte Formal"):
        if notas:
            with st.spinner("IA Redactando..."):
                # Simulación de llamada a Gemini (puedes configurar tu API Key en el paso siguiente)
                st.success("Asiento de Bitácora Generado:")
                st.markdown(f"""
                **PROYECTO:** Club Hawai  
                **RESUMEN TÉCNICO:** Se procedió con las labores de {notas}. Se verifica cumplimiento de normas COVENIN...
                """)
        else:
            st.warning("Por favor escribe notas de la obra.")
