import streamlit as st

# 1. Configuración de Alta Visibilidad
st.set_page_config(
    page_title="HM RENDERING - Control de Obra", 
    layout="wide"
)

# CSS Optimizado para Contraste y Legibilidad
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: #000000; }

    /* Fondo de la página */
    .stApp { background-color: #ffffff; }

    /* Cabecera Negra con Contraste Total */
    .brand-header {
        background-color: #000000;
        color: #ffffff !important;
        padding: 40px;
        border-radius: 0 0 25px 25px;
        text-align: center;
        margin-bottom: 30px;
    }
    .brand-header h1 { color: #ffffff !important; font-weight: 800; letter-spacing: 4px; margin: 0; }
    .brand-header p { color: #ffffff !important; font-weight: 300; letter-spacing: 2px; opacity: 0.9; }

    /* Métricas con Bordes Definidos */
    div[data-testid="stMetric"] {
        background-color: #f1f3f5;
        border: 2px solid #000000;
        padding: 20px;
        border-radius: 12px;
    }
    label[data-testid="stMetricLabel"] { color: #000000 !important; font-weight: 700 !important; font-size: 14px !important; }
    div[data-testid="stMetricValue"] { color: #000000 !important; font-weight: 800 !important; }

    /* Tarjetas Técnicas */
    .tech-card {
        background-color: #ffffff;
        border: 1px solid #000000;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .tech-title { color: #000000; font-weight: 700; text-transform: uppercase; font-size: 12px; margin-bottom: 5px; border-bottom: 1px solid #ddd; }
    .tech-value { color: #000000; font-size: 16px; font-weight: 500; }

    /* Pestañas (Tabs) con Texto Claro */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f8f9fa;
        border-radius: 5px 5px 0 0;
        color: #000000 !important;
        font-weight: 600;
    }

    /* Firma Final */
    .footer-signature {
        margin-top: 50px;
        padding: 30px;
        border-top: 3px solid #000000;
        text-align: center;
        background-color: #f8f9fa;
    }
    .signature-name { font-size: 18px; font-weight: 800; color: #000000; margin-bottom: 0; }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
st.markdown("""
    <div class="brand-header">
        <h1>HM RENDERING</h1>
        <p>STUDIO 3D | INGENIERÍA Y DISEÑO</p>
    </div>
    """, unsafe_allow_html=True)

# --- RESUMEN DE PROYECTO ---
st.markdown("### 📍 PROYECTO: CLUB HAWAI")
st.markdown("**Control de Ejecución de Losa Nervada (E=20cm)**")

# Métricas de Alto Contraste
c1, c2, c3, c4 = st.columns(4)
c1.metric("ÁREA TOTAL", "265.00 m²")
c2.metric("CONCRETO f'c", "210 kg/cm²")
c3.metric("ACERO fy", "4.200 kg/cm²")
c4.metric("ESPESOR", "20 cm")

st.markdown("---")

# --- CONTENIDO TÉCNICO ---
t1, t2, t3 = st.tabs(["📐 DETALLES DE PLANO", "🗓️ CRONOGRAMA", "🤖 ASISTENTE IA"])

with t1:
    st.markdown("#### Especificaciones Técnicas (Plano E-01)")
    
    
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
            <div class="tech-card">
                <div class="tech-title">📦 ALIGERADO</div>
                <div class="tech-value">Bloque de Anime: 0.15m x 0.50m x 2.00m</div>
            </div>
            <div class="tech-card">
                <div class="tech-title">⛓️ REFUERZO DE TEMPERATURA</div>
                <div class="tech-value">Malla Electrosoldada 15x15 cm</div>
            </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
            <div class="tech-card">
                <div class="tech-title">🛡️ RECUBRIMIENTO</div>
                <div class="tech-value">Mínimo Libre: 2.00 cm</div>
            </div>
            <div class="tech-card">
                <div class="tech-title">🚧 NOTAS DE UNIÓN</div>
                <div class="tech-value">Varillas grifadas ligeramente en vigas de carga</div>
            </div>
        """, unsafe_allow_html=True)

with t2:
    st.markdown("#### Ruta de Ejecución Técnica")
    st.info("Puntos críticos de inspección basados en normas COVENIN.")
    
    with st.expander("1. ENCOFRADO Y NIVELES", expanded=True):
        st.write("✓ Verificación de camillas y parales.")
        st.write("✓ Nivelación de precisión según cota de proyecto.")
        st.progress(100)
    
    with st.expander("2. ARMADO Y COLOCACIÓN"):
        st.write("• Distribución de nervios y bloques de anime.")
        st.write("• Amarre de refuerzo longitudinal y malla.")
        st.progress(30)
        
    with st.expander("3. VACIADO Y VIBRADO"):
        st.write("• Uso obligatorio de vibradora de aguja.")
        st.write("• Toma de cilindros para ensayo de compresión.")
        st.progress(0)

with t3:
    st.markdown("#### Generador de Bitácora Profesional")
    input_text = st.text_area("Describa la actividad del día:", placeholder="Ej: Vaciado de 50m2 de losa en tramo A-B...")
    if st.button("REDACTAR INFORME TÉCNICO"):
        st.markdown(f"""
        **ASIENTO DE BITÁCORA - CLUB HAWAI** *HM RENDERING STUDIO 3D* ---  
        **Actividad:** {input_text}  
        **Observaciones:** Ejecución conforme a planos. Se garantiza recubrimiento mínimo de 2cm y vibrado mecánico.
        """)

# --- FIRMA PROFESIONAL ---
st.markdown(f"""
    <div class="footer-signature">
        <p style="letter-spacing: 2px; color: #666; font-size: 12px; margin-bottom: 5px;">PROYECTO ELABORADO POR:</p>
        <p class="signature-name">Ing. Willians Hernández</p>
        <p style="color: #000; font-weight: 600;">CIV 267.515</p>
        <p style="font-size: 11px; margin-top: 20px; color: #999;">© 2026 TINACO, ESTADO COJEDES | VENEZUELA</p>
    </div>
    """, unsafe_allow_html=True)
