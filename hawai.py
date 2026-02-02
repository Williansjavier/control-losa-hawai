import streamlit as st
import pandas as pd
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Dashboard Losa Club Hawai",
    page_icon="HMRenderigStudio3D-[Recuperado].gif", # LOGO DE MARCA COMO ICONO
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
    
    /* REGLA MAESTRA DE TEXTO: Todo negro por defecto */
    h1, h2, h3, h4, h5, h6, p, div, span, label, li, 
    .stMarkdown, .stTextInput input, .stSelectbox, .stTextArea textarea {
        color: #111827 !important;
    }

    /* 2. HEADER TIPO BANNER */
    .header-image-container {
        width: 100%;
        border-radius: 0px 0px 15px 15px; 
        overflow: hidden;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stImage { margin-bottom: 20px; }
    .block-container { padding-top: 2rem !important; }

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

    /* 4. EXPANDERS */
    div[data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        color: #000000 !important;
        margin-bottom: 10px;
    }
    .streamlit-expanderHeader p { font-weight: 700 !important; font-size: 15px !important; color: #111827 !important; }
    .streamlit-expanderHeader svg { fill: #111827 !important; }

    /* 5. TABS (CORREGIDO) */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 6px;
        border: 1px solid #e5e7eb;
        padding: 8px 20px;
        font-weight: 600;
        font-size: 14px;
    }
    /* Estilo para tab seleccionado */
    .stTabs [aria-selected="true"] {
        background-color: #111827 !important;
        border-color: #111827;
    }
    /* EXCEPCIÓN CRÍTICA: Texto BLANCO en tab seleccionado */
    .stTabs [aria-selected="true"] p {
        color: #ffffff !important;
    }
    
    /* 6. TABLAS FINANCIERAS */
    .financial-total {
        font-size: 20px;
        font-weight: 900;
        text-align: right;
        padding: 15px;
        background-color: #f9fafb;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        margin-top: 10px;
    }
    .financial-total span {
        color: #059669; /* Verde Dinero */
    }

    /* 7. FOOTER */
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

# --- DATOS FINANCIEROS (NUEVO) ---
DATA_NERVADA = [
    {"MATERIAL": "CEMENTO GRIS PORTLAND TIPO I", "UND": "SACOS", "CANTIDAD": 159, "PRECIO ($)": 13.5, "TOTAL ($)": 2146.50},
    {"MATERIAL": "PIEDRA PICADA", "UND": "M3", "CANTIDAD": 19, "PRECIO ($)": 35, "TOTAL ($)": 665.00},
    {"MATERIAL": "ARENA LAVADA", "UND": "M3", "CANTIDAD": 8, "PRECIO ($)": 25, "TOTAL ($)": 200.00},
    {"MATERIAL": "BLOQUE ANIME 15X60X200", "UND": "UND", "CANTIDAD": 175, "PRECIO ($)": 15, "TOTAL ($)": 2625.00},
    {"MATERIAL": "MALLA ELECTROSOLDADA 15X15CM", "UND": "ROLLO", "CANTIDAD": 4, "PRECIO ($)": 100, "TOTAL ($)": 400.00},
    {"MATERIAL": "VARILLA 3/8 L=6M (NERVIOS)", "UND": "UND", "CANTIDAD": 116, "PRECIO ($)": 7, "TOTAL ($)": 812.00},
    {"MATERIAL": "CERCHA ELECTROSOLDADA 15CM L=6M", "UND": "UND", "CANTIDAD": 58, "PRECIO ($)": 10, "TOTAL ($)": 580.00},
]

DATA_METALICA = [
    {"MATERIAL": "CEMENTO GRIS PORTLAND TIPO I", "UND": "SACOS", "CANTIDAD": 13.5, "PRECIO ($)": 114, "TOTAL ($)": 1539.00},
    {"MATERIAL": "PIEDRA PICADA", "UND": "M3", "CANTIDAD": 35, "PRECIO ($)": 16, "TOTAL ($)": 560.00},
    {"MATERIAL": "ARENA LAVADA", "UND": "M3", "CANTIDAD": 25, "PRECIO ($)": 6, "TOTAL ($)": 150.00},
    {"MATERIAL": "CORREAS 120X60 ESP. 3mm", "UND": "UND", "CANTIDAD": 66, "PRECIO ($)": 70, "TOTAL ($)": 4620.00},
    {"MATERIAL": "MALLA ELECTROSOLDADA 15X15CM", "UND": "ROLLO", "CANTIDAD": 4, "PRECIO ($)": 100, "TOTAL ($)": 400.00},
    {"MATERIAL": "METALDECK CAL 22", "UND": "UND", "CANTIDAD": 79, "PRECIO ($)": 70, "TOTAL ($)": 5530.00},
]

# --- INTERFAZ PRINCIPAL ---

# 1. HEADER TIPO BANNER
header_url = "https://drive.google.com/uc?export=view&id=1rgnj8vDVR7w8gUcpGztnLhMJZ4KI6scO"
try:
    st.image(header_url, use_container_width=True)
except:
    st.error("Error cargando imagen header.")

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
# AÑADIDOS ICONOS A LOS NOMBRES DE LAS PESTAÑAS
tab1, tab2, tab3 = st.tabs(["📅 CRONOGRAMA", "📦 MATERIALES", "💰 ANÁLISIS FINANCIERO"])

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

# --- TAB 3: ANÁLISIS FINANCIERO ---
with tab3:
    st.markdown("### 💰 Tabla Comparativa de Costos")
    
    # Cálculos Totales (Basados en la imagen)
    # Losa Nervada Base (Comunes)
    total_comunes_nervada = 2146.50 + 665.00 + 200.00 + 2625.00 + 400.00
    costo_varilla = 812.00
    costo_cercha = 580.00
    
    total_nervada_varilla = total_comunes_nervada + costo_varilla
    total_nervada_cercha = total_comunes_nervada + costo_cercha
    total_metalica = 12799.00
    
    # Layout de Columnas para Tablas
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        st.markdown("#### 1. Losa Nervada (Concreto)")
        df_nervada = pd.DataFrame(DATA_NERVADA)
        
        # Formatear columnas numéricas
        st.dataframe(
            df_nervada.style.format({"PRECIO ($)": "{:.2f}", "TOTAL ($)": "{:.2f}"}),
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown(f"""
            <div class="financial-total">
                Total con Varillas 3/8": <span>${total_nervada_varilla:,.2f}</span><br>
                <span style="font-size:16px; color:#374151; font-weight:600;">Total con Cerchas: ${total_nervada_cercha:,.2f}</span>
            </div>
        """, unsafe_allow_html=True)

    with col_der:
        st.markdown("#### 2. Estructura Metálica")
        df_metalica = pd.DataFrame(DATA_METALICA)
        
        st.dataframe(
            df_metalica.style.format({"PRECIO ($)": "{:.2f}", "TOTAL ($)": "{:.2f}"}),
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown(f"""
            <div class="financial-total">
                Total Estructura Metálica: <span style="color:#dc2626;">${total_metalica:,.2f}</span>
            </div>
        """, unsafe_allow_html=True)

    st.divider()
    
    # Gráfico Comparativo Rápido
    st.markdown("#### 📊 Comparativa Visual")
    chart_data = pd.DataFrame({
        "Sistema Constructivo": ["Losa Nervada (Cercha)", "Losa Nervada (Varilla)", "Estructura Metálica"],
        "Costo Total ($)": [total_nervada_cercha, total_nervada_varilla, total_metalica]
    })
    st.bar_chart(chart_data, x="Sistema Constructivo", y="Costo Total ($)", color=["#059669"])

    st.warning("⚠️ **NOTA IMPORTANTE:** ESTOS COSTOS NO INCLUYEN TRANSPORTE Y ESTÁN EXENTOS DE GASTOS RELACIONADOS A MANO DE OBRA.")

# --- SIDEBAR LIMPIO ---
with st.sidebar:
    try:
        st.image("HMRenderigStudio3D-[Recuperado].gif", use_container_width=True)
    except:
        pass
    st.markdown("### Configuración")
    st.caption("Ajustes del proyecto")
