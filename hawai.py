import streamlit as st
import pandas as pd
import google.generativeai as genai
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Dashboard Losa Club Hawai",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# --- ESTILOS CSS CORRECTIVOS ---
st.markdown("""
    <style>
    /* 1. RESETEO TOTAL DE COLORES (FUERZA BRUTA MODO CLARO) */
    :root {
        --primary-color: #000000;
        --background-color: #f4f4f5;
        --secondary-background-color: #ffffff;
        --text-color: #111827;
        --font: "Source Sans Pro", sans-serif;
    }
    .stApp { background-color: #f4f4f5 !important; color: #111827 !important; }
    header[data-testid="stHeader"] { background-color: #f4f4f5 !important; }
    section[data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e5e7eb; }
    
    h1, h2, h3, h4, h5, h6, p, div, span, label, li, 
    .stMarkdown, .stTextInput input, .stSelectbox, .stTextArea textarea {
        color: #111827 !important;
    }

    /* 2. HEADER TIPO BANNER */
    .header-image-container {
        width: 100%;
        border-radius: 0px 0px 15px 15px; /* Bordes redondeados solo abajo */
        overflow: hidden;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stImage {
        margin-bottom: 20px;
    }
    /* Eliminar padding superior extra de Streamlit para que el banner suba */
    .block-container {
        padding-top: 2rem !important;
    }

    /* 3. TARJETAS KPI (GRID) */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 15px;
        margin-bottom: 25px;
    }
    .kpi-card {
        background-color: white;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 12px 18px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
        display: flex;
        align-items: center;
        transition: all 0.2s ease;
    }
    .kpi-card:hover {
        border-color: #111827;
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .kpi-icon {
        background-color: #f3f4f6;
        border-radius: 8px;
        width: 38px;
        height: 38px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        margin-right: 15px;
        color: #000 !important;
    }
    .kpi-content { display: flex; flex-direction: column; }
    .kpi-label { font-size: 11px; font-weight: 700; text-transform: uppercase; color: #6b7280 !important; margin-bottom: 2px; }
    .kpi-value { font-size: 18px; font-weight: 900; color: #111827 !important; }

    /* 4. EXPANDERS (RUTA CRÍTICA) */
    div[data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        color: #000000 !important;
        margin-bottom: 10px;
    }
    .streamlit-expanderHeader p { font-weight: 700 !important; font-size: 15px !important; color: #111827 !important; }
    .streamlit-expanderHeader svg { fill: #111827 !important; }

    /* 5. TABS */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 6px;
        border: 1px solid #e5e7eb;
        padding: 8px 20px;
        font-weight: 600;
        font-size: 14px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #111827 !important;
        color: white !important;
        border-color: #111827;
    }
    
    /* 6. FOOTER */
    .custom-footer {
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #e5e7eb;
        text-align: center;
        font-size: 12px;
        color: #6b7280 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATOS DEL PROYECTO ---
PROJECT_DATA = {
    "name": "CLUB HAWAI",
    "area": 265,
    "type": "Losa Nervada (e=20cm)",
    "strength": "f'c 210",
    "duration": "17 Días"
}

ACTIVITIES = [
    {"id": 1, "title": "Encofrado", "icon": "🏗️", "duration": "5 Días", "desc": "Nivelación, parales y camillas."},
    {"id": 2, "title": "Acero y Bloques", "icon": "⛓️", "duration": "4 Días", "desc": "Colocación de anime, nervios y malla."},
    {"id": 3, "title": "Vaciado", "icon": "🚛", "duration": "1 Día", "desc": "Vaciado f'c 210 kg/cm², vibrado."},
    {"id": 4, "title": "Curado", "icon": "💧", "duration": "7 Días", "desc": "Hidratación continua."}
]

# --- FUNCIONES DE IA ---
def get_gemini_response(api_key, prompt):
    if not api_key: return "⚠️ Requiere API Key."
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash') 
        response = model.generate_content(prompt)
        return response.text
    except Exception as e: return f"Error: {str(e)}"

# --- INTERFAZ PRINCIPAL ---

# 1. HEADER TIPO BANNER (IMAGEN DRIVE)
# ID del archivo extraído de tu link: 1rgnj8vDVR7w8gUcpGztnLhMJZ4KI6scO
# Convertido a link de visualización directa
header_url = "https://drive.google.com/uc?export=view&id=1rgnj8vDVR7w8gUcpGztnLhMJZ4KI6scO"

try:
    st.image(header_url, use_container_width=True)
except:
    st.error("No se pudo cargar la imagen. Asegúrate de que el enlace de Drive tenga permisos de 'Cualquiera con el enlace'.")

st.markdown(f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <h2 style="margin:0; font-size: 24px; font-weight:900; letter-spacing:-0.5px;">CONTROL DE OBRA: {PROJECT_DATA['name']}</h2>
        <p style="margin:0; font-size:14px; color:#6b7280 !important; font-weight:600;">EJECUCIÓN DE LOSA ENTREPISO NERVADA</p>
    </div>
""", unsafe_allow_html=True)

# 2. KPIS
kpi_html = f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-icon">📐</div>
        <div class="kpi-content">
            <span class="kpi-label">Área Total</span>
            <span class="kpi-value">{PROJECT_DATA['area']} m²</span>
        </div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">⏱️</div>
        <div class="kpi-content">
            <span class="kpi-label">Duración Est.</span>
            <span class="kpi-value">{PROJECT_DATA['duration']}</span>
        </div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">🧱</div>
        <div class="kpi-content">
            <span class="kpi-label">Resistencia</span>
            <span class="kpi-value">{PROJECT_DATA['strength']}</span>
        </div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">📏</div>
        <div class="kpi-content">
            <span class="kpi-label">Espesor Losa</span>
            <span class="kpi-value">20 cm</span>
        </div>
    </div>
</div>
"""
st.markdown(kpi_html, unsafe_allow_html=True)

# 3. CONTENIDO
tab1, tab2, tab3 = st.tabs(["CRONOGRAMA", "MATERIALES", "ASISTENTE IA"])

# --- TAB 1: CRONOGRAMA ---
with tab1:
    col_cron, col_rec = st.columns([2, 1])
    with col_cron:
        st.markdown("##### 📅 Ruta Crítica")
        for act in ACTIVITIES:
            with st.expander(f"{act['icon']} {act['title']} ({act['duration']})"):
                st.markdown(f"**Detalle:** {act['desc']}")
                st.progress(0)
    with col_rec:
        st.markdown("##### ⚠️ Notas Técnicas")
        st.info("""
        - **Vibrado:** Obligatorio durante vaciado.
        - **Grifado:** Acero en vigas.
        - **Curado:** Mínimo 7 días.
        """)

# --- TAB 2: MATERIALES ---
with tab2:
    st.markdown("##### 📦 Inventario")
    opt = st.radio("Opciones de Refuerzo:", ["A: Varilla 3/8\"", "B: Cercha"], horizontal=True)
    
    data = [
        {"M": "Cemento Gris", "Cant": "159 Sacos"},
        {"M": "Piedra Picada", "Cant": "19 m³"},
        {"M": "Arena Lavada", "Cant": "8 m³"},
        {"M": "Bloque Anime", "Cant": "175 Pzas"},
        {"M": "Malla Electrosoldada", "Cant": "4 Rollos"},
    ]
    if "Varilla" in opt:
        data.append({"M": "Varilla 3/8\" (L=6m)", "Cant": "116 Pzas"})
    else:
        data.append({"M": "Cercha 15cm", "Cant": "58 Pzas"})
        
    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

# --- TAB 3: IA ---
with tab3:
    st.markdown("##### 🤖 Asistente Técnico")
    if not st.session_state.get("api_key_input"):
         st.session_state.api_key_input = st.text_input("API Key (Google):", type="password")
    
    nota = st.text_area("Bitácora Diaria:", height=80, placeholder="Escribe aquí las incidencias del día...")
    if st.button("Generar Reporte", type="primary"):
        with st.spinner("Generando..."):
            res = get_gemini_response(st.session_state.api_key_input, f"Reporte obra civil: {nota}")
            st.success(res)

# --- FOOTER ---
st.markdown("""
    <div class="custom-footer">
        <b>Elaborado Por: Ing. Willians Hernández</b> (CIV 267.515)<br>
        © 2024 HM Rendering Studio 3D
    </div>
""", unsafe_allow_html=True)
