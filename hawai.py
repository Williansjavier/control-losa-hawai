import streamlit as st
import pandas as pd
import google.generativeai as genai
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Dashboard Losa Club Hawai",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS ROBUSTOS (FORZANDO TEMA CLARO) ---
st.markdown("""
    <style>
    /* 1. FORZAR FONDO Y TEXTO GENERAL (Estilo Modo Claro) */
    [data-testid="stAppViewContainer"] {
        background-color: #f3f4f6; /* Gris muy suave */
    }
    [data-testid="stHeader"] {
        background-color: #f3f4f6;
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff; /* Sidebar blanco */
        border-right: 1px solid #e5e7eb;
    }
    
    /* Forzar color de texto negro/gris oscuro para todo */
    .stApp, .stMarkdown, p, h1, h2, h3, h4, h5, h6, span, div, label, .stSelectbox, .stTextInput {
        color: #1f2937 !important; 
        font-family: 'Source Sans Pro', sans-serif;
    }

    /* 2. TARJETAS (KPIs) - Replica del diseño React */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb;
        padding: 20px !important;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        color: #1f2937;
    }
    div[data-testid="stMetricLabel"] {
        color: #6b7280 !important; /* Gris medio para etiquetas */
        font-size: 14px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
    }
    div[data-testid="stMetricValue"] {
        color: #111827 !important; /* Negro fuerte para números */
        font-size: 28px !important;
        font-weight: 800 !important;
    }

    /* 3. LOGO HEXAGONAL PERSONALIZADO */
    .logo-container {
        display: flex;
        align-items: center;
        margin-bottom: 25px;
        padding-bottom: 20px;
        border-bottom: 2px solid #e5e7eb;
    }
    .hexagon {
        width: 60px;
        height: 60px;
        background-color: #111827; /* Negro casi puro */
        color: white !important;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 20px;
        clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
        margin-right: 15px;
    }
    .brand-title {
        font-size: 24px;
        font-weight: 900;
        line-height: 1;
        color: #111827 !important;
        margin: 0;
    }
    .brand-subtitle {
        font-size: 12px;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #6b7280 !important;
        margin: 0;
    }

    /* 4. TABS Y EXPANDERS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border-radius: 6px;
        border: 1px solid #e5e7eb;
        color: #4b5563;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #111827 !important;
        color: white !important;
    }
    
    /* Estilo para los expanders (Acordeón) */
    .streamlit-expanderHeader {
        background-color: white !important;
        border: 1px solid #e5e7eb;
        color: #111827 !important;
        font-weight: 600;
        border-radius: 8px;
    }
    
    /* 5. FIRMA */
    .signature-box {
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #e5e7eb;
        text-align: center;
    }
    .signature-text {
        color: #4b5563 !important;
        font-size: 13px;
    }
    .signature-name {
        color: #111827 !important;
        font-weight: bold;
        display: block;
        margin-top: 5px;
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
        return "⚠️ CONFIGURACIÓN REQUERIDA: Por favor ingresa tu API Key de Google Gemini en la barra lateral izquierda."
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash') 
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

# --- INTERFAZ PRINCIPAL ---

# 1. HEADER CON LOGO ESTILO REACT
st.markdown("""
    <div class="logo-container">
        <div class="hexagon">HM</div>
        <div>
            <h1 class="brand-title">HM RENDERING</h1>
            <p class="brand-subtitle">STUDIO 3D</p>
        </div>
        <div style="margin-left: auto; text-align: right;">
            <h3 style="margin:0; font-size:18px; font-weight:bold; color:#1f2937;">PROYECTO CLUB HAWAI</h3>
            <span style="font-size:12px; color:#6b7280;">EJECUCIÓN LOSA ENTREPISO</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# 2. SIDEBAR
with st.sidebar:
    st.header("⚙️ Panel de Control")
    api_key = st.text_input("🔑 Gemini API Key", type="password", help="Pega aquí tu clave para activar la IA")
    
    st.markdown("### 📋 Ficha Técnica")
    st.success(f"""
    **Tipo:** {PROJECT_DATA['type']}
    **Área:** {PROJECT_DATA['area']} m²
    **Concreto:** {PROJECT_DATA['strength']}
    """)
    
    # FIRMA
    st.markdown("""
        <div class="signature-box">
            <span class="signature-text">Desarrollado Por:</span>
            <span class="signature-name">Ing. Willians Hernandez</span>
            <span class="signature-text">CIV 267.515</span>
        </div>
    """, unsafe_allow_html=True)

# 3. KPIS (TARJETAS)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Área Total", f"{PROJECT_DATA['area']} m²")
col2.metric("Tiempo Estimado", PROJECT_DATA['duration'])
col3.metric("Resistencia Concreto", "210 kg/cm²")
col4.metric("Espesor Losa", "20 cm")

st.markdown("<br>", unsafe_allow_html=True)

# 4. CONTENIDO PRINCIPAL
tab1, tab2, tab3 = st.tabs(["📅 CRONOGRAMA", "📦 MATERIALES", "✨ ASISTENTE IA"])

# --- TAB 1: CRONOGRAMA ---
with tab1:
    st.subheader("Ruta Crítica de Ejecución")
    
    col_act_1, col_act_2 = st.columns([2, 1])
    
    with col_act_1:
        for activity in ACTIVITIES:
            with st.expander(f"{activity['title']} ⏱️ {activity['duration']}", expanded=True):
                st.write(f"**Descripción:** {activity['desc']}")
                st.progress(0) # Barra visual estática
    
    with col_act_2:
        st.info("""
        **⚠️ Recomendaciones Técnicas:**
        
        * **Vibrado:** Vibrar el concreto con aguja durante el vaciado.
        * **Acero:** Grifar varillas en intersecciones viga-columna.
        * **Curado:** Mantener húmedo por 7 días.
        """)

# --- TAB 2: MATERIALES ---
with tab2:
    col_ctrl, col_display = st.columns([1, 2])
    
    with col_ctrl:
        st.markdown("### Configuración de Refuerzo")
        reinforcement_opt = st.radio(
            "Seleccione tipo de nervio:",
            ("Opción A: Varilla 3/8\"", "Opción B: Cercha Electrosoldada"),
            help="Cambia el cálculo de materiales según el refuerzo elegido."
        )
    
    with col_display:
        st.markdown("### 📋 Inventario de Materiales")
        
        # Datos base
        materials_data = [
            {"Material": "Cemento Gris Portland", "Uso": "Concreto", "Cantidad": "159 Sacos"},
            {"Material": "Piedra Picada", "Uso": "Agregado Grueso", "Cantidad": "19 m³"},
            {"Material": "Arena Lavada", "Uso": "Agregado Fino", "Cantidad": "8 m³"},
            {"Material": "Bloque Anime (15x60x200)", "Uso": "Aligeramiento", "Cantidad": "175 Pzas"},
            {"Material": "Malla Electrosoldada", "Uso": "Acero Temperatura", "Cantidad": "4 Rollos"}
        ]
        
        # Lógica
        if "Opción A" in reinforcement_opt:
            materials_data.append({"Material": "Varilla 3/8\" (L=6m)", "Uso": "Refuerzo Nervios", "Cantidad": "116 Pzas"})
            st.toast("Calculando para Varillas...", icon="🏗️")
        else:
            materials_data.append({"Material": "Cercha 15cm (L=6m)", "Uso": "Refuerzo Nervios", "Cantidad": "58 Pzas"})
            st.toast("Calculando para Cerchas...", icon="🏗️")
            
        df_materials = pd.DataFrame(materials_data)
        st.dataframe(df_materials, use_container_width=True, hide_index=True)

# --- TAB 3: ASISTENTE IA ---
with tab3:
    st.markdown("### 🤖 Asistente de Obra Inteligente (Gemini)")
    
    col_ai_1, col_ai_2 = st.columns(2)
    
    # Generador de Bitácora
    with col_ai_1:
        with st.container(border=True):
            st.markdown("#### 📔 Generador de Bitácora")
            st.caption("Escribe notas rápidas (ej: llovió, falta material) y genera un reporte formal.")
            
            notes = st.text_area("Notas del día:", height=100)
            
            if st.button("Generar Reporte Formal", type="primary"):
                with st.spinner("Redactando bitácora..."):
                    prompt_report = f"""
                    Actúa como el Ing. Residente Willians Hernandez. 
                    Redacta un asiento formal para el LIBRO DE OBRA del proyecto {PROJECT_DATA['name']}.
                    Notas crudas: "{notes}".
                    Usa lenguaje técnico, menciona 'Incidencias' y 'Conclusiones'.
                    """
                    report_result = get_gemini_response(api_key, prompt_report)
                    st.markdown(report_result)

    # Analista de Seguridad
    with col_ai_2:
        with st.container(border=True):
            st.markdown("#### 🛡️ Análisis de Riesgos")
            st.caption("Selecciona una actividad para obtener el plan de seguridad.")
            
            activity_selected = st.selectbox("Actividad:", [act['title'] for act in ACTIVITIES])
            
            if st.button("Analizar Seguridad"):
                with st.spinner("Consultando normas de seguridad..."):
                    prompt_safety = f"""
                    Para la actividad "{activity_selected}" en una losa nervada:
                    Lista 3 riesgos críticos y el EPP obligatorio. Sé breve y directo.
                    """
                    safety_result = get_gemini_response(api_key, prompt_safety)
                    st.success(f"Análisis para: {activity_selected}")
                    st.markdown(safety_result)
