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

# --- ESTILOS CSS AVANZADOS (ANIMACIONES + TARJETAS CUSTOM + FIX VISIBILIDAD) ---
st.markdown("""
    <style>
    /* 1. ANIMACIÓN DE ENTRADA (DINAMISMO) */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translate3d(0, 20px, 0);
        }
        to {
            opacity: 1;
            transform: translate3d(0, 0, 0);
        }
    }
    
    /* Aplicar animación a los contenedores principales */
    .element-container, .stMarkdown, .stExpander {
        animation: fadeInUp 0.6s ease-out forwards;
    }

    /* 2. ESTILOS GENERALES (MODO CLARO FORZADO) */
    [data-testid="stAppViewContainer"] { background-color: #f3f4f6; }
    [data-testid="stHeader"] { background-color: #f3f4f6; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e5e7eb; }
    
    h1, h2, h3, h4, h5, h6, p, span, div, label, li, .stMarkdown {
        color: #111827 !important;
        font-family: 'Source Sans Pro', sans-serif;
    }

    /* 3. TARJETAS KPI PERSONALIZADAS (HTML/CSS) */
    .kpi-card {
        background-color: white;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border-left: 5px solid #111827; /* Acento negro */
        display: flex;
        align-items: center;
        margin-bottom: 10px;
        transition: transform 0.2s;
    }
    .kpi-card:hover {
        transform: translateY(-2px); /* Efecto levitación al pasar mouse */
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .kpi-icon {
        background-color: #f3f4f6;
        border-radius: 50%;
        width: 45px;
        height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        margin-right: 15px;
        color: #111827;
    }
    .kpi-content {
        flex-grow: 1;
    }
    .kpi-label {
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        color: #6b7280 !important;
        margin-bottom: 2px;
    }
    .kpi-value {
        font-size: 20px;
        font-weight: 900;
        color: #111827 !important;
        line-height: 1.2;
    }

    /* 4. HEADER CON IMAGEN */
    .header-container {
        display: flex;
        align-items: center;
        background-color: white;
        padding: 15px 25px;
        border-radius: 15px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        margin-bottom: 25px;
    }
    .header-text {
        margin-left: 20px;
        flex-grow: 1;
    }
    .header-title {
        font-size: 24px;
        font-weight: 900;
        margin: 0;
        line-height: 1;
    }
    .header-subtitle {
        font-size: 14px;
        color: #6b7280 !important;
        font-weight: 600;
    }

    /* 5. CORRECCIÓN ROBUSTA DE EXPANDERS (RUTA CRÍTICA) */
    /* Fondo blanco y borde suave */
    div[data-testid="stExpander"] {
        background-color: white !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    /* Cabecera siempre visible */
    div[data-testid="stExpander"] details summary {
        color: #111827 !important;
    }
    /* Texto del título dentro del summary: NEGRO IMPORTANTE */
    div[data-testid="stExpander"] details summary p, 
    div[data-testid="stExpander"] details summary span,
    div[data-testid="stExpander"] details summary div {
        color: #000000 !important; 
        font-weight: 700 !important;
        font-size: 15px !important;
        opacity: 1 !important;
    }
    /* Icono de la flecha */
    div[data-testid="stExpander"] details summary svg {
        color: #111827 !important;
        fill: #111827 !important;
    }
    /* Fondo al pasar el mouse */
    div[data-testid="stExpander"] details summary:hover {
        background-color: #f9fafb !important;
    }

    /* 6. TABS */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 6px;
        border: 1px solid #e5e7eb;
        padding: 8px 16px;
        font-size: 14px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #111827 !important;
        color: white !important;
    }
    
    /* 7. FOOTER */
    .main-footer {
        margin-top: 40px;
        padding: 20px;
        border-top: 1px solid #e5e7eb;
        text-align: center;
        font-size: 13px;
        color: #6b7280;
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
    {"id": 1, "title": "Montaje de Encofrado", "icon": "🏗️", "duration": "5 Días", "desc": "Nivelación, colocación de parales y tendido de camillas."},
    {"id": 2, "title": "Armado de Bloques y Acero", "icon": "⛓️", "duration": "4 Días", "desc": "Colocación de bloques de anime, armado de nervios y malla."},
    {"id": 3, "title": "Vaciado de Concreto", "icon": "🚛", "duration": "1 Día", "desc": "Vaciado monolítico f'c 210 kg/cm², vibrado y regleado."},
    {"id": 4, "title": "Curado de Concreto", "icon": "💧", "duration": "7 Días", "desc": "Riego continuo de agua para hidratación."}
]

# --- FUNCIONES DE IA (GEMINI) ---
def get_gemini_response(api_key, prompt):
    if not api_key:
        return "⚠️ CONFIGURACIÓN: Ingresa tu API Key en la barra lateral para usar la IA."
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash') 
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

# --- INTERFAZ PRINCIPAL ---

# 1. HEADER CON LOGO (IMAGEN REAL)
# Usamos columnas de Streamlit para insertar la imagen correctamente
col_h_img, col_h_txt = st.columns([1, 5])
with col_h_img:
    try:
        # Intenta cargar la imagen subida. Si no existe localmente, muestra un placeholder.
        st.image("HMRenderigStudio3D-[Recuperado].gif", width=120) 
    except:
        st.markdown("<div style='font-size:40px; text-align:center;'>🏗️</div>", unsafe_allow_html=True)

with col_h_txt:
    st.markdown(f"""
        <div style="padding-top: 10px;">
            <h1 style="margin:0; font-size: 28px; font-weight:900;">HM RENDERING STUDIO 3D</h1>
            <p style="margin:0; font-size:16px; color:#4b5563 !important; font-weight:600;">PROYECTO: {PROJECT_DATA['name']} | EJECUCIÓN LOSA ENTREPISO</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 2. SIDEBAR
with st.sidebar:
    st.header("⚙️ Configuración")
    api_key = st.text_input("🔑 Gemini API Key", type="password")
    
    st.success(f"""
    **📋 Ficha Técnica**
    
    * **Tipo:** {PROJECT_DATA['type']}
    * **Área:** {PROJECT_DATA['area']} m²
    * **F'c:** {PROJECT_DATA['strength']}
    """)
    st.markdown("---")
    st.caption("v2.0 - Dashboard Interactivo")

# 3. KPIS PERSONALIZADOS (HTML/CSS) - MÁS PEQUEÑOS Y CON ICONOS
# Usamos st.markdown con HTML puro para tener control total del diseño de las tarjetas
kpi_html = f"""
<div style="display: flex; gap: 15px; flex-wrap: wrap; margin-bottom: 20px;">
    
    <div style="flex: 1; min-width: 200px;" class="kpi-card">
        <div class="kpi-icon">📐</div>
        <div class="kpi-content">
            <div class="kpi-label">Área Total</div>
            <div class="kpi-value">{PROJECT_DATA['area']} m²</div>
        </div>
    </div>

    <div style="flex: 1; min-width: 200px;" class="kpi-card">
        <div class="kpi-icon">⏱️</div>
        <div class="kpi-content">
            <div class="kpi-label">Tiempo Est.</div>
            <div class="kpi-value">{PROJECT_DATA['duration']}</div>
        </div>
    </div>

    <div style="flex: 1; min-width: 200px;" class="kpi-card">
        <div class="kpi-icon">🧱</div>
        <div class="kpi-content">
            <div class="kpi-label">Concreto</div>
            <div class="kpi-value">210 kg/cm²</div>
        </div>
    </div>

    <div style="flex: 1; min-width: 200px;" class="kpi-card">
        <div class="kpi-icon">📏</div>
        <div class="kpi-content">
            <div class="kpi-label">Espesor</div>
            <div class="kpi-value">20 cm</div>
        </div>
    </div>

</div>
"""
st.markdown(kpi_html, unsafe_allow_html=True)

# 4. CONTENIDO PRINCIPAL (TABS)
tab1, tab2, tab3 = st.tabs(["📅 CRONOGRAMA", "📦 MATERIALES", "✨ ASISTENTE IA"])

# --- TAB 1: CRONOGRAMA ---
with tab1:
    st.subheader("Ruta Crítica de Ejecución")
    
    col_act_1, col_act_2 = st.columns([2, 1])
    
    with col_act_1:
        # Aquí se aplica la animación de entrada secuencial visual
        for i, activity in enumerate(ACTIVITIES):
            # Usamos un expander con título reforzado en CSS
            with st.expander(f"{activity['icon']}  {activity['title']}  |  ⏱️ {activity['duration']}", expanded=True):
                st.markdown(f"""
                <div style="padding: 5px 0;">
                    <p style="margin-bottom: 5px; font-size: 14px;">{activity['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.progress(0)

    with col_act_2:
        with st.container(border=True):
            st.markdown("#### ⚠️ Recomendaciones")
            st.markdown("""
            * **Vibrado:** Uso de aguja 100% obligatorio.
            * **Acero:** Grifado en intersecciones.
            * **Curado:** Mantener húmedo 7 días.
            """)

# --- TAB 2: MATERIALES ---
with tab2:
    col_ctrl, col_display = st.columns([1, 2])
    
    with col_ctrl:
        st.markdown("#### 🛠️ Configuración")
        reinforcement_opt = st.radio(
            "Seleccione Refuerzo:",
            ("Opción A: Varilla 3/8\"", "Opción B: Cercha"),
            horizontal=False
        )
    
    with col_display:
        st.markdown("#### 📋 Inventario Requerido")
        
        base_materials = [
            {"Icon": "🧪", "Material": "Cemento Gris", "Uso": "Concreto", "Cant": "159 Sacos"},
            {"Icon": "🪨", "Material": "Piedra Picada", "Uso": "Agregado", "Cant": "19 m³"},
            {"Icon": "🏖️", "Material": "Arena Lavada", "Uso": "Agregado", "Cant": "8 m³"},
            {"Icon": "⬜", "Material": "Bloque Anime", "Uso": "Aligerado", "Cant": "175 Pzas"},
            {"Icon": "🕸️", "Material": "Malla Electrosoldada", "Uso": "Temperatura", "Cant": "4 Rollos"}
        ]
        
        if "Opción A" in reinforcement_opt:
            base_materials.append({"Icon": "📏", "Material": "Varilla 3/8\" (L=6m)", "Uso": "Nervios", "Cant": "116 Pzas"})
        else:
            base_materials.append({"Icon": "🏗️", "Material": "Cercha 15cm (L=6m)", "Uso": "Nervios", "Cant": "58 Pzas"})
            
        df = pd.DataFrame(base_materials)
        st.dataframe(
            df, 
            column_config={
                "Icon": st.column_config.TextColumn(""),
                "Material": st.column_config.TextColumn("Material", width="medium"),
                "Cant": st.column_config.TextColumn("Cantidad", width="small"),
            },
            use_container_width=True, 
            hide_index=True
        )

# --- TAB 3: ASISTENTE IA ---
with tab3:
    st.markdown("### 🤖 Asistente Técnico (Gemini)")
    
    col_ai_1, col_ai_2 = st.columns(2)
    
    with col_ai_1:
        st.info("📝 **Generador de Bitácora:**")
        notes = st.text_area("Notas del día:", height=100, placeholder="Ej: Se completó el encofrado del eje A-B...")
        if st.button("Generar Reporte", type="primary", use_container_width=True):
            with st.spinner("Redactando..."):
                prompt = f"Como Ing. Civil, redacta un asiento de bitácora para {PROJECT_DATA['name']} usando estas notas: {notes}."
                st.markdown(get_gemini_response(api_key, prompt))

    with col_ai_2:
        st.warning("🛡️ **Análisis de Seguridad:**")
        act = st.selectbox("Actividad:", [a['title'] for a in ACTIVITIES])
        if st.button("Analizar Riesgos", use_container_width=True):
            with st.spinner("Analizando..."):
                prompt = f"Lista 3 riesgos críticos y EPP para: {act}."
                st.markdown(get_gemini_response(api_key, prompt))

# --- FOOTER ---
st.markdown("""
    <div class="main-footer">
        <strong>Elaborado Por: Ing. Willians Hernandez</strong><br>
        <span>CIV 267.515</span><br><br>
        <span style="font-size:11px">© 2024 HM Rendering Studio 3D</span>
    </div>
""", unsafe_allow_html=True)
