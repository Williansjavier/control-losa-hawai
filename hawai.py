import streamlit as st
import pandas as pd
import google.generativeai as genai
from datetime import date
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Dashboard Losa Club Hawai",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS PERSONALIZADOS (NEGRO/BLANCO/GRIS) ---
st.markdown("""
    <style>
    /* Ajustes generales para tema monocromático */
    .stApp {
        background-color: #f3f4f6;
        color: #1f2937;
    }
    .main-header {
        font-family: 'Helvetica', sans-serif;
        color: #111827;
    }
    
    /* Estilo para las tarjetas de métricas */
    div[data-testid="stMetric"] {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #000;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }
    
    /* Logo Hexagonal CSS */
    .hexagon-wrapper {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 20px;
    }
    .hexagon {
        width: 50px;
        height: 55px;
        background: black;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 18px;
        clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
    }
    .brand-text h1 {
        margin: 0;
        font-size: 24px;
        font-weight: 800;
        line-height: 1;
        color: #111827;
    }
    .brand-text span {
        font-size: 12px;
        letter-spacing: 2px;
        color: #6b7280;
        text-transform: uppercase;
    }
    
    /* Firma del Ingeniero */
    .engineer-signature {
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #e5e7eb;
        font-size: 12px;
        color: #4b5563;
        text-align: center;
    }
    .engineer-name {
        font-weight: bold;
        color: #111827;
        display: block;
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
    {"id": 1, "title": "Montaje de Encofrado y Apuntalamiento", "duration": "5 Días", "desc": "Nivelación, colocación de parales y tendido de camillas."},
    {"id": 2, "title": "Armado de Bloques y Acero", "duration": "4 Días", "desc": "Colocación de bloques de anime, armado de nervios y malla."},
    {"id": 3, "title": "Vaciado de Concreto", "duration": "1 Día", "desc": "Vaciado monolítico f'c 210 kg/cm², vibrado y regleado."},
    {"id": 4, "title": "Curado de Concreto", "duration": "7 Días", "desc": "Riego continuo de agua para hidratación."}
]

# --- FUNCIONES DE IA (GEMINI) ---
def get_gemini_response(api_key, prompt):
    if not api_key:
        return "⚠️ Por favor ingresa tu API Key de Google Gemini en la barra lateral."
    
    try:
        genai.configure(api_key=api_key)
        # Usamos el modelo flash para rapidez
        model = genai.GenerativeModel('gemini-2.0-flash') 
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al conectar con Gemini: {str(e)}"

# --- INTERFAZ PRINCIPAL ---

# 1. HEADER / LOGO
st.markdown("""
    <div class="hexagon-wrapper">
        <div class="hexagon">HM</div>
        <div class="brand-text">
            <h1>HM RENDERING</h1>
            <span>STUDIO 3D</span>
        </div>
    </div>
""", unsafe_allow_html=True)

st.title(f"Ejecución de Losa: {PROJECT_DATA['name']}")
st.markdown("---")

# 2. SIDEBAR (Configuración y Firma)
with st.sidebar:
    st.header("⚙️ Configuración")
    api_key = st.text_input("Gemini API Key", type="password", help="Necesaria para el asistente IA")
    
    st.markdown("---")
    st.markdown("### 📋 Ficha Técnica")
    st.info(f"""
    **Tipo:** {PROJECT_DATA['type']}
    **Área:** {PROJECT_DATA['area']} m²
    **Concreto:** {PROJECT_DATA['strength']}
    """)
    
    # FIRMA DEL INGENIERO (SOLICITADA)
    st.markdown("""
        <div class="engineer-signature">
            <span class="engineer-name">Elaborado Por:</span>
            Ing. Willians Hernandez<br>
            CIV 267515
        </div>
    """, unsafe_allow_html=True)

# 3. KPIS (Métricas Clave)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Área Total", f"{PROJECT_DATA['area']} m²", delta_color="off")
col2.metric("Tiempo Estimado", PROJECT_DATA['duration'], delta_color="off")
col3.metric("Resistencia Concreto", "210 kg/cm²", delta_color="off")
col4.metric("Espesor Losa", "20 cm", delta_color="off")

st.markdown("---")

# 4. PESTAÑAS PRINCIPALES
tab1, tab2, tab3 = st.tabs(["📅 Cronograma", "📦 Materiales", "✨ Asistente IA"])

# --- TAB 1: CRONOGRAMA ---
with tab1:
    st.subheader("Ruta Crítica de Ejecución")
    
    for activity in ACTIVITIES:
        with st.expander(f"{activity['title']} ({activity['duration']})", expanded=True):
            st.write(activity['desc'])
            # Barra de progreso visual simple
            st.progress(0, text="Estado: Pendiente")

    st.markdown("### 📝 Notas Técnicas")
    st.warning("""
    * **Vibrado:** Vibrar el concreto con aguja durante el vaciado.
    * **Intersecciones:** Grifar ligeramente varillas en intersecciones viga-columna.
    * **Curado:** Mantener curado húmedo por 7 días mínimo.
    """)

# --- TAB 2: MATERIALES ---
with tab2:
    col_ctrl, col_display = st.columns([1, 3])
    
    with col_ctrl:
        st.subheader("Opciones de Refuerzo")
        reinforcement_opt = st.radio(
            "Seleccione tipo de nervio:",
            ("Opción A: Varilla 3/8\"", "Opción B: Cercha Electrosoldada")
        )
    
    with col_display:
        st.subheader("Inventario de Materiales")
        
        # Datos base
        materials_data = [
            {"Material": "Cemento Gris Portland", "Uso": "Concreto", "Cantidad": "159 Sacos"},
            {"Material": "Piedra Picada", "Uso": "Agregado Grueso", "Cantidad": "19 m³"},
            {"Material": "Arena Lavada", "Uso": "Agregado Fino", "Cantidad": "8 m³"},
            {"Material": "Bloque Anime (15x60x200)", "Uso": "Aligeramiento", "Cantidad": "175 Pzas"},
            {"Material": "Malla Electrosoldada", "Uso": "Acero Temperatura", "Cantidad": "4 Rollos"}
        ]
        
        # Lógica condicional
        if "Opción A" in reinforcement_opt:
            materials_data.append({"Material": "Varilla 3/8\" (L=6m)", "Uso": "Refuerzo Nervios", "Cantidad": "116 Pzas"})
        else:
            materials_data.append({"Material": "Cercha 15cm (L=6m)", "Uso": "Refuerzo Nervios", "Cantidad": "58 Pzas"})
            
        df_materials = pd.DataFrame(materials_data)
        st.table(df_materials)

# --- TAB 3: ASISTENTE IA ---
with tab3:
    st.subheader("Asistente de Obra Inteligente (Gemini)")
    
    col_ai_1, col_ai_2 = st.columns(2)
    
    # Generador de Bitácora
    with col_ai_1:
        st.markdown("#### 📔 Generador de Bitácora")
        st.caption("Escribe notas rápidas y la IA redactará un asiento formal.")
        
        notes = st.text_area("Notas del día:", height=150, placeholder="Ej: Llovió a las 2pm, se vació medio camión, faltó un albañil...")
        
        if st.button("Generar Reporte Formal"):
            with st.spinner("Redactando bitácora..."):
                prompt_report = f"""
                Actúa como un Ingeniero Civil Residente (Ing. Willians Hernandez). 
                Redacta un asiento formal para el LIBRO DE OBRA del proyecto {PROJECT_DATA['name']}.
                Notas crudas: "{notes}".
                Estructura: Encabezado, Actividades, Incidencias, Conclusión. Tono técnico.
                """
                report_result = get_gemini_response(api_key, prompt_report)
                st.markdown("---")
                st.markdown(report_result)

    # Analista de Seguridad
    with col_ai_2:
        st.markdown("#### 🛡️ Análisis de Riesgos")
        st.caption("Selecciona una actividad para obtener un plan de seguridad.")
        
        activity_selected = st.selectbox("Actividad a analizar:", [act['title'] for act in ACTIVITIES])
        
        if st.button("Analizar Seguridad"):
            with st.spinner("Analizando riesgos..."):
                prompt_safety = f"""
                Para la actividad: "{activity_selected}" en construcción de losa nervada.
                Genera: 1. Tres riesgos críticos. 2. EPP Obligatorio. 3. Regla de Oro.
                Formato Markdown.
                """
                safety_result = get_gemini_response(api_key, prompt_safety)
                st.success(f"Análisis para: {activity_selected}")
                st.markdown(safety_result)

# Footer
st.markdown("---")
st.markdown("© 2024 HM Rendering Studio 3D - Todos los derechos reservados.")
