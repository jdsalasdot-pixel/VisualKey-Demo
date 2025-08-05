import streamlit as st

# Configuración inicial de la app
st.set_page_config(page_title="VisualKey Demo", page_icon="🎬", layout="wide")

# Inicializar session_state global (compartido entre páginas)
if 'adaptive_ready' not in st.session_state:
    st.session_state.adaptive_ready = False
if 'environment' not in st.session_state:
    st.session_state.environment = None
if 'token_valid' not in st.session_state:
    st.session_state.token_valid = False
if 'playing' not in st.session_state:
    st.session_state.playing = False
if 'mode' not in st.session_state:
    st.session_state.mode = None
if 'watermark_id' not in st.session_state:
    st.session_state.watermark_id = None
if 'log' not in st.session_state:
    st.session_state.log = []
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'  # Detección simple de tema; ajusta si necesitas.

# Sidebar para navegación y info
st.sidebar.title("Navegación VisualKey")
st.sidebar.radio("Pasos:", ["1. Environment Scan", "2. Authentication", "3. Playback", "4. Audit Log"], key="nav")
st.sidebar.markdown("---")
st.sidebar.info("Demo de VisualKey: Protección adaptativa para contenido audiovisual. Desarrollado por Juan Diego Salas Rueda.")

# Nota: Streamlit maneja multi-páginas automáticamente con la carpeta pages/.
# El contenido principal se carga en cada página individual.
