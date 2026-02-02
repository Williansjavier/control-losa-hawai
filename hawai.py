import streamlit as st
import pandas as pd

# 1. Configuración de la Aplicación y Estética Superior
st.set_page_config(
    page_title="HM RENDERING - Dashboard de Control", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Estilo CSS para paleta Gris, Blanco y Negro con acabados elegantes
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&family=Roboto+Mono:wght@300&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    .main { background-color: #ffffff; }
    
    /* Header & Branding */
    .brand-container {
        background-color: #000000;
        color: #ffffff;
        padding: 2rem;
        border-radius: 0px 0px 20px 20px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .brand-logo { font-size: 3rem; font-weight: 700; letter-spacing: 5px; margin-bottom: 0; }
    .brand-subtitle { font-size: 0.9rem; font-weight: 300; letter-spacing: 3px; color: #cccccc; text-transform: uppercase; }
    
    /* Metrics & Cards */
    div[data-testid="stMetric"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .tech-card {
        background-color: #ffffff;
        border-left: 4px solid #333333;
        padding: 1.2rem;
        margin-bottom: 1rem;
        border-radius: 4px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
    }
    .spec-label { font-size: 0.75rem; color: #666666; font-weight: 700; text-transform: uppercase; }
    .spec-value { font-size: 1.1rem; color: #000000; font-family: 'Roboto Mono', monospace; }
    
    /* Footer */
    .footer {
        margin-top: 4rem;
        padding: 2rem;
        border-top: 1px solid #eeeeee;
        text-align: center;
        color: #999999;
    }
    .signature { color: #000000; font-weight: 700; font-size: 1.1rem; }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA DE MARCA ---
st.markdown("""
    <div class="brand-container">
        <p class="brand-logo">HM</p>
        <p class="brand-subtitle">Rendering Studio 3D</p>
    </div>
    """, unsafe_allow_html=True)

# --- PANEL LATERAL DE CONTROL ---
with st.sidebar:
    st.markdown("### ⚙️ PARÁMETROS DE OBRA")
    area_input = st.number_input("ÁREA TOTAL (m²)", value=265.0, step=1.0)
    st.divider()
    st.markdown("#### PROYECTO: **CLUB HAWAI**")
    st.caption("Detalle: Losa Nervada en un sentido (E=20cm)")

# --- CUERPO PRINCIPAL ---
st.markdown(f"#### 📊 CONTROL TÉCNICO ESTRATÉGICO")
st.caption("Resumen ejecutivo de materiales y especificaciones del plano E-01")

# Métricas de Diseño
c1, c2, c3, c4 = st.columns(4)
c1.metric("ÁREA PROYECTADA", f"{area_input} m²")
c2.metric("CONCRETO f'c", "210 kg/cm²")
c3.metric("ACERO fy", "4200 kg/cm²")
c4.metric("ESPESOR (E)", "0.20 m")

# Organización por Pestañas Técnicas
tab_espec, tab_ruta, tab_bit = st.tabs(["📐 ESPECIFICACIONES", "🏗️ RUTA DE OBRA", "🤖 ASISTENTE IA"])

with tab_espec:
    st.markdown("##### DETALLES CONSTRUCTIVOS (PLANO E-01)")
    
    

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="tech-card">
                <p class="spec-label">Aligeramiento</p>
                <p class="spec-value">Bloque Anime: 0.15m x 0.50m x 2.00m</p>
            </div>
            <div class="tech-card">
                <p class="spec-label">Refuerzo Temperatura</p>
                <p class="spec-value">Malla Electrosoldada 15x15 cm</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="tech-card">
                <p class="spec-label">Recubrimientos</p>
                <p class="spec-value">Mínimo: 2.00 cm Libres</p>
            </div>
            <div class="tech-card">
                <p class="spec-label">Técnica de Vibrado</p>
                <p class="spec-value">Vibrador de aguja (Obligatorio)</p>
            </div>
        """, unsafe_allow_html=True)

with tab_ruta:
    st.markdown("##### CRONOGRAMA DE EJECUCIÓN")
    with st.expander("FASE 1: ENCOFRADO Y NIVELES", expanded=True):
        st.write("Verificación de cotas y apuntalamiento según plano de envigado.")
        st.progress(25)
    with st.expander("FASE 2: ARMADO Y MALLA"):
        st.write("Colocación de nervios y bloques de anime. Grifado de varillas en uniones.")
        st.progress(0)
    with st.expander("FASE 3: VACIADO Y CONTROL"):
        st.write("Vaciado monolítico f'c 210. Toma de probetas para ensayo.")
        st.progress(0)

with tab_bit:
    st.markdown("##### GENERADOR TÉCNICO DE BITÁCORA")
    notas_campo = st.text_area("REGISTRO DE INCIDENCIAS:", placeholder="Ej: Culminación de acero de refuerzo en Eje 1-4...")
    if st.button("REDACTAR INFORME"):
        st.success("INFORME GENERADO:")
        st.code(f"PROYECTO: CLUB HAWAI\nFASE: EJECUCIÓN DE LOSA\nOBSERVACIÓN: {notas_campo}\nESTADO: Conforme a Plano E-01")

# --- PIE DE PÁGINA PROFESIONAL ---
st.markdown(f"""
    <div class="footer">
        <p>Dashboard de Gestión de Proyectos de Ingeniería</p>
        <p class="signature">Elaborado por el Ing. Willians Hernández</p>
        <p>CIV 267.515</p>
        <br>
        <p style="font-size: 0.7rem;">© 2026 HM RENDERING STUDIO 3D - TINACO, COJEDES</p>
    </div>
    """, unsafe_allow_html=True)
