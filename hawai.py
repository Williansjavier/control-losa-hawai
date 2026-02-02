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

# --- ESTILOS CSS CORRECTIVOS (FORZADO DE MODO CLARO TOTAL) ---
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
    
    /* Fondo General de la App */
    .stApp {
        background-color: #f4f4f5 !important;
        color: #111827 !important;
    }
    
    /* Header superior */
    header[data-testid="stHeader"] {
        background-color: #f4f4f5 !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e5e7eb;
    }
    
    /* REGLA MAESTRA DE TEXTO: Todo negro, sin excepción */
    h1, h2, h3, h4, h5, h6, p, div, span, label, li, 
    .stMarkdown, .stTextInput input, .stSelectbox, .stTextArea textarea {
        color: #111827 !important;
    }

    /* 2. TARJETAS KPI (REDUCIDAS Y COMPACTAS) */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 10px;
        margin-bottom: 20px;
    }
    .kpi-card {
        background-color: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 10px 15px; /* Padding reducido */
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        display: flex;
        align-items: center;
        transition: transform 0.2s;
    }
    .kpi-card:hover {
        border-color: #000;
        transform: translateY(-2px);
    }
    .kpi-icon {
        background-color: #f3f4f6;
        border-radius: 6px;
        width: 32px; /* Más pequeño */
        height: 32px; /* Más pequeño */
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        margin-right: 12px;
        color: #000 !important;
    }
    .kpi-content {
        display: flex;
        flex-direction: column;
    }
    .kpi-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        color: #6b7280 !important;
        line-height: 1;
        margin-bottom: 4px;
    }
    .kpi-value {
        font-size: 16px; /* Texto más compacto */
        font-weight: 800;
        color: #111827 !important;
        line-height: 1;
    }

    /* 3. MENÚS DESPLEGABLES (EXPANDERS) - CORRECCIÓN DE FONDO NEGRO */
    div[data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        color: #000000 !important;
    }
    
    /* Cabecera del expander */
    .streamlit-expanderHeader {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-bottom: 1px solid #f0f0f0;
    }
    
    /* Texto del título del expander */
    .streamlit-expanderHeader p {
        font-weight: 700 !important;
        font-size: 15px !important;
    }

    /* Contenido interno del expander */
    div[data-testid="stExpander"] div[role="group"] {
        background-color: #ffffff !important;
    }
    
    /* Icono de flecha */
    .streamlit-expanderHeader svg {
        color: #000000 !important;
        fill: #000000 !important;
    }

    /* 4. ANIMACIÓN DE CASCADA (DINAMISMO) */
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stExpander, .kpi-card, .element-container {
        animation: slideIn 0.5s ease-out forwards;
    }

    /* 5. TABS */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        gap: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border-radius: 6px;
        color: #4b5563 !important;
        border: 1px solid #e5e7eb;
        padding: 6px 16px;
        font-size: 13px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #000000 !important;
        color: #ffffff !important;
        border-color: #000000;
    }
    .stTabs [aria-selected="true"] p {
        color: #ffffff !important;
    }
    
    /* 6. FOOTER */
    .custom-footer {
        margin-top: 30px;
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
    "type": "Losa Nervada (e=20cm)", # Texto acortado para móvil
    "strength": "f'c 210",
    "duration": "17 Días"
}

ACTIVITIES = [
    {"id": 1, "title": "Encofrado", "icon": "🏗️", "duration": "5 Días", "desc": "Nivelación, parales y camillas."},
    {"id": 2, "title": "Acero y Bloques", "icon": "⛓️", "duration": "4 Días", "desc": "Colocación de anime, nervios y malla."},
    {"id": 3, "title": "Vaciado", "icon": "🚛", "duration": "1 Día", "desc": "Vaciado f'c 210 kg/cm², vibrado."},
    {"id": 4, "title": "Curado", "icon": "💧", "duration": "7 Días", "desc": "Hidratación continua."}
]

# --- FUNCIONES DE IA (GEMINI) ---
def get_gemini_response(api_key, prompt):
    if not api_key:
        return "⚠️ Requiere API Key."
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash') 
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# --- INTERFAZ PRINCIPAL ---

# 1. HEADER INTEGRADO
col_logo, col_title = st.columns([1, 6])
with col_logo:
    # Intenta cargar la imagen, si falla usa un emoji grande
    try:
        st.image("HMRenderigStudio3D-[Recuperado].gif", width=80) 
    except:
        st.markdown("<div style='font-size:40px;'>🏗️</div>", unsafe_allow_html=True)

with col_title:
    st.markdown(f"""
        <div style="margin-left: 10px;">
            <h2 style="margin:0; font-size: 22px; font-weight:900; letter-spacing:-0.5px;">HM RENDERING STUDIO 3D</h2>
            <p style="margin:0; font-size:13px; color:#6b7280 !important; font-weight:600;">PROYECTO: {PROJECT_DATA['name']} | CONTROL DE OBRA</p>
        </div>
    """, unsafe_allow_html=True)

st.write("") # Espacio

# 2. KPIS COMPACTOS (Nuevo Diseño Grid)
kpi_html = f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-icon">📐</div>
        <div class="kpi-content">
            <span class="kpi-label">Área</span>
            <span class="kpi-value">{PROJECT_DATA['area']} m²</span>
        </div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">⏱️</div>
        <div class="kpi-content">
            <span class="kpi-label">Tiempo</span>
            <span class="kpi-value">{PROJECT_DATA['duration']}</span>
        </div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">🧱</div>
        <div class="kpi-content">
            <span class="kpi-label">Concreto</span>
            <span class="kpi-value">{PROJECT_DATA['strength']}</span>
        </div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">📏</div>
        <div class="kpi-content">
            <span class="kpi-label">Espesor</span>
            <span class="kpi-value">20 cm</span>
        </div>
    </div>
</div>
"""
st.markdown(kpi_html, unsafe_allow_html=True)

# 3. CONTENIDO PRINCIPAL
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
        st.markdown("##### ⚠️ Notas")
        st.info("""
        - **Vibrado:** Obligatorio.
        - **Grifado:** En vigas.
        - **Curado:** 7 días.
        """)

# --- TAB 2: MATERIALES ---
with tab2:
    st.markdown("##### 📦 Inventario")
    
    # Selector compacto
    opt = st.radio("Refuerzo:", ["A: Varilla 3/8\"", "B: Cercha"], horizontal=True)
    
    data = [
        {"M": "Cemento", "Cant": "159 Sacos"},
        {"M": "Piedra", "Cant": "19 m³"},
        {"M": "Arena", "Cant": "8 m³"},
        {"M": "Anime", "Cant": "175 Pzas"},
        {"M": "Malla", "Cant": "4 Rollos"},
    ]
    
    if "Varilla" in opt:
        data.append({"M": "Varilla 3/8\"", "Cant": "116 Pzas"})
    else:
        data.append({"M": "Cercha", "Cant": "58 Pzas"})
        
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)

# --- TAB 3: IA ---
with tab3:
    st.markdown("##### 🤖 Asistente Gemini")
    
    # Campo para la API Key aquí si no está en sidebar
    if not st.session_state.get("api_key_input"):
         st.session_state.api_key_input = st.text_input("API Key (Google):", type="password")

    nota = st.text_area("Bitácora:", height=70, placeholder="Ej: Llovió hoy...")
    if st.button("Generar Reporte", type="primary"):
        with st.spinner("..."):
            res = get_gemini_response(st.session_state.api_key_input, f"Reporte obra civil corto: {nota}")
            st.success(res)

# --- SIDEBAR LIMPIO ---
with st.sidebar:
    try:
        st.image("HMRenderigStudio3D-[Recuperado].gif", use_container_width=True)
    except:
        pass
    st.markdown("### Configuración")
    st.caption("Ajustes del proyecto")

# --- FOOTER ---
st.markdown("""
    <div class="custom-footer">
        <b>Elaborado Por: Ing. Willians Hernández</b> (CIV 267.515)<br>
        © 2024 HM Rendering Studio 3D
    </div>
""", unsafe_allow_html=True)
