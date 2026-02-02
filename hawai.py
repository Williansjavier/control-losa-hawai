import streamlit as st
import pandas as pd

# 1. Configuración de la App
st.set_page_config(
    page_title="HM RENDERING - Dashboard Club Hawai", 
    layout="wide"
)

# 2. Estilo CSS de Alto Contraste (Gris, Blanco, Negro)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: #000000; }
    .stApp { background-color: #ffffff; }

    /* Cabecera Negra Premium */
    .brand-header {
        background-color: #000000;
        color: #ffffff !important;
        padding: 40px;
        border-radius: 0 0 25px 25px;
        text-align: center;
        margin-bottom: 30px;
    }
    .brand-header h1 { color: #ffffff !important; font-weight: 800; letter-spacing: 4px; margin: 0; }
    .brand-header p { color: #ffffff !important; font-weight: 300; letter-spacing: 2px; }

    /* Métricas con Contraste Total */
    div[data-testid="stMetric"] {
        background-color: #f1f3f5;
        border: 2px solid #000000;
        padding: 20px;
        border-radius: 12px;
    }
    label[data-testid="stMetricLabel"] { color: #000000 !important; font-weight: 700 !important; }
    div[data-testid="stMetricValue"] { color: #000000 !important; font-weight: 800 !important; }

    /* Tarjetas de Materiales y Detalles */
    .tech-card {
        background-color: #ffffff;
        border: 1px solid #000000;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .tech-title { color: #000000; font-weight: 700; text-transform: uppercase; font-size: 11px; border-bottom: 1px solid #eee; }
    .tech-value { color: #000000; font-size: 15px; font-weight: 600; margin-top: 5px; }

    /* Footer / Firma */
    .footer-signature {
        margin-top: 50px;
        padding: 30px;
        border-top: 3px solid #000000;
        text-align: center;
        background-color: #f8f9fa;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
st.markdown("""
    <div class="brand-header">
        <h1>HM RENDERING</h1>
        <p>STUDIO 3D | GESTIÓN DE PROYECTOS DE INGENIERÍA</p>
    </div>
    """, unsafe_allow_html=True)

# --- DATOS DEL PROYECTO (Recuperando tu contenido original) ---
st.markdown("### 🏗️ PROYECTO: CLUB HAWAI")
st.markdown("**Losa Nervada en un Sentido (e=20cm) | f'c = 210 kg/cm²**")

# Métricas Principales
c1, c2, c3, c4 = st.columns(4)
c1.metric("ÁREA TOTAL", "265 m²")
c2.metric("TIEMPO EST.", "17 Días")
c3.metric("CONCRETO", "210 kg/cm²")
c4.metric("ESPESOR", "20 cm")

st.divider()

# --- CONTENIDO PRINCIPAL POR PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["📅 CRONOGRAMA", "📦 MATERIALES E INVENTARIO", "✨ ASISTENTE IA"])

with tab1:
    st.markdown("#### Ruta de Ejecución Técnica")
    # Restaurando tus actividades originales
    actividades = [
        {"fase": "1. Encofrado y Apuntalamiento", "dur": "5 Días", "desc": "Nivelación, parales y tendido de camillas."},
        {"fase": "2. Armado de Bloques y Acero", "dur": "4 Días", "desc": "Colocación de anime (15x50x200) y malla electrosoldada."},
        {"fase": "3. Vaciado de Concreto", "dur": "1 Día", "desc": "Vaciado monolítico con vibrado de aguja."},
        {"fase": "4. Curado de Concreto", "dur": "7 Días", "desc": "Riego continuo para garantizar resistencia."}
    ]
    for a in actividades:
        with st.expander(f"{a['fase']} ({a['dur']})"):
            st.write(a['desc'])
            st.progress(25)

with tab2:
    st.markdown("#### Inventario Estimado de Materiales")
    
    # Toggle de Refuerzo (Original)
    opcion_acero = st.radio("Seleccione Opción de Refuerzo en Nervios:", 
                            ["Opción A: Varilla 3/8\"", "Opción B: Cercha 15cm"])
    
    # Tabla de materiales base (Original)
    m_col1, m_col2 = st.columns(2)
    
    with m_col1:
        st.markdown(f"""
            <div class="tech-card"><div class="tech-title">Cemento Gris</div><div class="tech-value">159 Sacos</div></div>
            <div class="tech-card"><div class="tech-title">Piedra Picada</div><div class="tech-value">19 m³</div></div>
            <div class="tech-card"><div class="tech-title">Arena Lavada</div><div class="tech-value">8 m³</div></div>
        """, unsafe_allow_html=True)
    
    with m_col2:
        st.markdown(f"""
            <div class="tech-card"><div class="tech-title">Bloque de Anime (15x60x200)</div><div class="tech-value">175 Piezas</div></div>
            <div class="tech-card"><div class="tech-title">Malla Electrosoldada (15x15)</div><div class="tech-value">4 Rollos</div></div>
        """, unsafe_allow_html=True)

    # Detalle dinámico de acero
    if "Opción A" in opcion_acero:
        st.warning("⚠️ **REFUERZO SELECCIONADO:** 116 Piezas de Varilla 3/8\" (L=6m)")
    else:
        st.warning("⚠️ **REFUERZO SELECCIONADO:** 58 Piezas de Cercha 15cm (L=6m)")

with tab3:
    st.markdown("#### Asistente de Bitácora e Ingeniería")
    notas = st.text_area("Notas del día en obra:", placeholder="Ej: Se completó el 50% del encofrado...")
    
    if st.button("GENERAR REPORTE PARA CLIENTE"):
        if notas:
            st.success("ASIENTO DE BITÁCORA GENERADO:")
            st.info(f"**PROYECTO CLUB HAWAI**\n\n**Actividad:** {notas}\n\n**Observaciones Técnicas:** Se verifica cumplimiento de espesor de 20cm y uso de materiales certificados f'c 210. Ejecución supervisada por Ing. Willians Hernandez.")
        else:
            st.error("Por favor, ingrese notas para procesar.")

# --- FIRMA PROFESIONAL (Tu requerimiento) ---
st.markdown(f"""
    <div class="footer-signature">
        <p style="color: #666; font-size: 12px; letter-spacing: 2px;">DOCUMENTO TÉCNICO ELABORADO POR:</p>
        <p style="font-size: 20px; font-weight: 800; color: #000; margin-bottom: 0;">Ing. Willians Hernández</p>
        <p style="font-size: 16px; font-weight: 700; color: #000;">CIV 267.515</p>
        <p style="font-size: 11px; color: #999; margin-top: 20px;">© 2026 HM RENDERING STUDIO 3D | TINACO - COJEDES</p>
    </div>
    """, unsafe_allow_html=True)
