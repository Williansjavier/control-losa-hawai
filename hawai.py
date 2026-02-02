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

# --- ESTILOS CSS ROBUSTOS (RESPONSIVE + ALTO CONTRASTE) ---
st.markdown("""
    <style>
    /* 1. FORZAR MODO CLARO Y CONTRASTE EN TODO EL SITIO */
    [data-testid="stAppViewContainer"] {
        background-color: #f3f4f6;
    }
    [data-testid="stHeader"] {
        background-color: #f3f4f6;
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e7eb;
    }
    
    /* REGLA MAESTRA DE TEXTO: Fuerza negro casi puro en todo */
    h1, h2, h3, h4, h5, h6, p, span, div, label, li, 
    .stMarkdown, .stTextInput, .stSelectbox, .stRadio, 
    [data-testid="stWidgetLabel"], .stDataFrame, .stTable {
        color: #111827 !important; /* Negro tinta */
        font-family: 'Source Sans Pro', sans-serif;
    }
    
    /* Excepción para texto dentro de botones primarios (usualmente blanco) */
    button[kind="primary"] p, button[kind="primary"] span {
        color: #ffffff !important;
    }

    /* 2. TARJETAS (KPIs) */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 1px solid #d1d5db; /* Borde más visible */
        padding: 15px !important;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    div[data-testid="stMetricLabel"] {
        color: #4b5563 !important; /* Gris oscuro para etiquetas */
        font-weight: 700 !important;
    }
    div[data-testid="stMetricValue"] {
        color: #000000 !important; /* Negro puro para números */
    }

    /* 3. LOGO PERSONALIZADO (ADAPTABLE) */
    .logo-container {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 20px;
        border-bottom: 2px solid #e5e7eb;
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .hexagon {
        width: 50px;
        height: 50px;
        background-color: #000000;
        color: white !important;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        font-size: 18px;
        clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
        margin-right: 15px;
        flex-shrink: 0; /* Evita que el logo se aplaste */
    }
    .brand-info {
        flex-grow: 1;
    }
    .brand-title {
        font-size: 22px;
        font-weight: 900;
        line-height: 1.1;
        margin: 0;
    }
    .project-info {
        text-align: right;
    }

    /* 4. OPTIMIZACIÓN MÓVIL (MEDIA QUERIES) */
    @media only screen and (max-width: 768px) {
        .logo-container {
            flex-direction: column;
            align-items: flex-start;
            gap: 10px;
        }
        .project-info {
            text-align: left;
            margin-top: 5px;
            padding-top: 5px;
            border-top: 1px solid #eee;
            width: 100%;
        }
        div[data-testid="stMetric"] {
            margin-bottom: 10px; /* Separación entre tarjetas en móvil */
        }
        /* Ajuste de pestañas en móvil */
        .stTabs [data-baseweb="tab-list"] {
            flex-wrap: wrap; 
        }
        .stTabs [data-baseweb="tab"] {
            flex-grow: 1;
            text-align: center;
        }
    }

    /* 5. TABS Y ELEMENTOS UI */
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        color: #374151 !important;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #000000 !important;
        color: #ffffff !important;
        border-color: #000000;
    }
    .stTabs [aria-selected="true"] p {
        color: #ffffff !important;
    }

    /* 6. FOOTER FIRMA (ESTILO VISIBLE) */
    .main-footer {
        margin-top: 50px;
        padding: 20px;
        border-top: 2px solid #e5e7eb;
        text-align: center;
        background-color: #ffffff;
        border-radius: 8px;
    }
    .main-footer p {
        margin: 0;
        font-size: 14px;
        color: #4b5563 !important;
    }
    .main-footer strong {
        color: #000000 !important;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATOS DEL PROYECTO ---
PROJECT_DATA = {
    "name": "CLUB HAWAI",
    "area": 265,
    "type": "Losa Nervada en un Sentido (e=20cm)",
    "strength": "f'c = 210 kg/cm²",
    "duration": "~17 Días"
}

ACTIVITIES = [
    {"id": 1, "title": "1. Montaje de Encofrado", "duration": "5 Días", "desc": "Nivelación, colocación de parales y tendido de camillas."},
    {"id": 2, "title": "2. Armado de Bloques y Acero", "duration": "4 Días", "desc": "Colocación de bloques de anime, armado de nervios y malla."},
    {"id": 3, "title": "3. Vaciado de Concreto", "duration": "1 Día", "desc": "Vaciado monolítico f'c 210 kg/cm², vibrado y regleado."},
    {"id": 4, "title": "4. Curado de Concreto", "duration": "7 Días", "desc": "Riego continuo de agua para hidratación."}
]

# --- FUNCIONES DE IA (GEMINI) ---
def get_gemini_response(api_key, prompt):
    if not api_key:
        return "⚠️ AVISO: Ingresa tu API Key en el menú lateral (flecha arriba a la izquierda) para usar la IA."
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash') 
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"

# --- INTERFAZ PRINCIPAL ---

# 1. HEADER (Optimizado para Móvil)
st.markdown("""
    <div class="logo-container">
        <div class="hexagon">HM</div>
        <div class="brand-info">
            <h1 class="brand-title">HM RENDERING</h1>
            <span style="font-size:12px; letter-spacing:2px; text-transform:uppercase; font-weight:bold;">STUDIO 3D</span>
        </div>
        <div class="project-info">
            <div style="font-weight:900; font-size:16px;">PROYECTO CLUB HAWAI</div>
            <div style="font-size:12px; color:#4b5563;">EJECUCIÓN LOSA ENTREPISO</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 2. SIDEBAR
with st.sidebar:
    st.header("⚙️ Configuración")
    api_key = st.text_input("🔑 Gemini API Key", type="password", help="Necesaria para el asistente inteligente")
    
    st.markdown("### 📋 Ficha Técnica")
    st.info(f"""
    **Tipo:** {PROJECT_DATA['type']}
    **Área:** {PROJECT_DATA['area']} m²
    **Concreto:** {PROJECT_DATA['strength']}
    """)
    
    # Firma en Sidebar (Opcional, también está en el footer)
    st.markdown("---")
    st.caption("v1.2 Mobile Optimized")

# 3. KPIS (TARJETAS)
# Usamos columnas estándar, pero el CSS se encarga de que no se vean mal en móvil
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Área Total", f"{PROJECT_DATA['area']} m²")
kpi2.metric("Tiempo Total", PROJECT_DATA['duration'])
kpi3.metric("Resistencia", "210 kg/cm²")
kpi4.metric("Espesor", "20 cm")

st.markdown("<br>", unsafe_allow_html=True)

# 4. CONTENIDO PRINCIPAL
tab1, tab2, tab3 = st.tabs(["📅 CRONOGRAMA", "📦 MATERIALES", "✨ ASISTENTE IA"])

# --- TAB 1: CRONOGRAMA ---
with tab1:
    st.subheader("Ruta Crítica de Ejecución")
    
    col_act_1, col_act_2 = st.columns([2, 1])
    
    with col_act_1:
        for activity in ACTIVITIES:
            with st.expander(f"{activity['title']} ({activity['duration']})", expanded=True):
                st.markdown(f"**Descripción:** {activity['desc']}")
                st.progress(0)
    
    with col_act_2:
        with st.container(border=True):
            st.markdown("#### ⚠️ Recomendaciones")
            st.markdown("""
            * **Vibrado:** Uso obligatorio de aguja.
            * **Acero:** Grifar en intersecciones.
            * **Curado:** 7 días continuos.
            """)

# --- TAB 2: MATERIALES ---
with tab2:
    # En móvil, las columnas se apilan automáticamente
    col_ctrl, col_display = st.columns([1, 2])
    
    with col_ctrl:
        st.markdown("#### Configuración")
        reinforcement_opt = st.radio(
            "Tipo de Refuerzo:",
            ("Opción A: Varilla 3/8\"", "Opción B: Cercha"),
            help="Cambia el cálculo de materiales."
        )
    
    with col_display:
        st.markdown("#### 📋 Listado de Materiales")
        
        materials_data = [
            {"Material": "Cemento Gris Portland", "Uso": "Concreto", "Cantidad": "159 Sacos"},
            {"Material": "Piedra Picada", "Uso": "Agregado Grueso", "Cantidad": "19 m³"},
            {"Material": "Arena Lavada", "Uso": "Agregado Fino", "Cantidad": "8 m³"},
            {"Material": "Bloque Anime (15x60x200)", "Uso": "Aligeramiento", "Cantidad": "175 Pzas"},
            {"Material": "Malla Electrosoldada", "Uso": "Acero Temperatura", "Cantidad": "4 Rollos"}
        ]
        
        if "Opción A" in reinforcement_opt:
            materials_data.append({"Material": "Varilla 3/8\" (L=6m)", "Uso": "Refuerzo Nervios", "Cantidad": "116 Pzas"})
        else:
            materials_data.append({"Material": "Cercha 15cm (L=6m)", "Uso": "Refuerzo Nervios", "Cantidad": "58 Pzas"})
            
        df_materials = pd.DataFrame(materials_data)
        
        # Mostramos tabla estática para mejor legibilidad en móvil que dataframe interactivo
        st.table(df_materials)

# --- TAB 3: ASISTENTE IA ---
with tab3:
    st.markdown("### 🤖 Asistente de Obra (Gemini)")
    
    col_ai_1, col_ai_2 = st.columns(2)
    
    with col_ai_1:
        st.markdown("#### 📔 Bitácora Automática")
        notes = st.text_area("¿Qué pasó hoy en la obra?", height=100, placeholder="Ej: Se vaciaron 10m3 de concreto...")
        
        if st.button("Generar Reporte", type="primary", use_container_width=True):
            with st.spinner("Escribiendo..."):
                prompt = f"Como Ing. Residente, escribe un reporte formal de obra para {PROJECT_DATA['name']} basado en: {notes}. Incluye incidencias."
                res = get_gemini_response(api_key, prompt)
                st.info(res)

    with col_ai_2:
        st.markdown("#### 🛡️ Análisis de Seguridad")
        act = st.selectbox("Actividad:", [a['title'] for a in ACTIVITIES])
        
        if st.button("Analizar Riesgos", use_container_width=True):
            with st.spinner("Analizando..."):
                prompt = f"Lista 3 riesgos críticos y EPP para la actividad: {act}."
                res = get_gemini_response(api_key, prompt)
                st.success(res)

# --- FOOTER CON FIRMA (VISIBLE EN MÓVIL) ---
st.markdown("""
    <div class="main-footer">
        <p>Elaborado Por:</p>
        <strong>Ing. Willians Hernandez</strong>
        <p>CIV 267.515</p>
        <br>
        <p style="font-size:11px; opacity:0.7;">© 2024 HM Rendering Studio 3D</p>
    </div>
""", unsafe_allow_html=True)
