import streamlit as st
from datetime import datetime
import random
from PIL import Image, ImageDraw, ImageFont

# Configuración inicial de la app
st.set_page_config(page_title="VisualKey Demo", page_icon="🎬", layout="wide")
st.title("🎬 VisualKey – Prototipo de Playback Seguro Adaptativo")
st.info("Flujo secuencial para probar VisualKey: Ingresa token → Valida entorno → Reproduce → Simula piratería (opcional) → Revisa logs.")

# Token-to-environment mapping
VALID_TOKENS = {
    "premium123": "Premium",
    "standard123": "Standard",
    "compat123": "Compatibility"
}

# Inicializar session_state
if 'step' not in st.session_state:
    st.session_state.step = 1  # 1: Token, 2: Entorno, 3: Reproducción, 4: Finalizado
if 'token_valid' not in st.session_state:
    st.session_state.token_valid = False
if 'environment_valid' not in st.session_state:
    st.session_state.environment_valid = False
if 'playing' not in st.session_state:
    st.session_state.playing = False
if 'mode' not in st.session_state:
    st.session_state.mode = None
if 'watermark_id' not in st.session_state:
    st.session_state.watermark_id = None
if 'log' not in st.session_state:
    st.session_state.log = []

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generate_watermark_id():
    return ''.join(random.choices('0123456789ABCDEF', k=8))

@st.cache_data
def create_watermark_image(wm_text, mode):
    img = Image.new("RGB", (640, 360), color=(20, 20, 20))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), wm_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_color = (255, 0, 0) if mode == 'Compatibility' else (150, 150, 150)
    x = (img.width - text_width) // 2 if mode == 'Compatibility' else img.width - text_width - 10
    y = (img.height - text_height) // 2 if mode == 'Compatibility' else img.height - text_height - 10

    draw.text((x, y), wm_text, font=font, fill=text_color)
    return img

# Paso 1: Validación de Token
with st.expander("🔐 Paso 1: Autenticación de Acceso", expanded=st.session_state.step == 1):
    if st.session_state.step == 1:
        token_input = st.text_input("Ingresa tu token de acceso:", type="password", key="token_input")
        if st.button("Validar Token"):
            if token_input in VALID_TOKENS:
                st.session_state.mode = VALID_TOKENS[token_input]
                st.session_state.token_valid = True
                st.session_state.step = 2
                st.session_state.log.append(f"{timestamp()}: Token válido '{token_input}' aceptado para modo tentativo {st.session_state.mode}")
                st.success("Token validado. Procede a validar el entorno.")
                st.rerun()
            else:
                st.session_state.log.append(f"{timestamp()}: Intento de token inválido – {token_input}")
                st.error("Token inválido. Intenta nuevamente.")

# Paso 2: Validación del Entorno
if st.session_state.token_valid:
    with st.expander("🔍 Paso 2: Escaneo de Entorno del Dispositivo", expanded=st.session_state.step == 2):
        if st.session_state.step == 2:
            option = st.selectbox("Selecciona entorno simulado:", [
                "Dispositivo Seguro Verificado (Premium)",
                "Red Hogar Confiable (Standard)",
                "VPN / Red Desconocida (Compatibility)"
            ], key="env_select")
            if st.button("Validar Entorno"):
                if "Seguro" in option:
                    environment = "Premium"
                elif "Hogar" in option:
                    environment = "Standard"
                else:
                    environment = "Compatibility"
                
                allowed_modes = ["Premium", "Standard", "Compatibility"]
                if allowed_modes.index(st.session_state.mode) >= allowed_modes.index(environment):
                    st.session_state.environment_valid = True
                    st.session_state.watermark_id = generate_watermark_id()
                    st.session_state.playing = True
                    st.session_state.step = 3
                    st.session_state.log.append(f"{timestamp()}: Entorno validado como {environment}. Modo final: {st.session_state.mode}")
                    st.session_state.log.append(f"{timestamp()}: Watermark ID generado = {st.session_state.watermark_id}")
                    st.success("Entorno seguro. Iniciando reproducción.")
                    st.rerun()
                else:
                    st.session_state.log.append(f"{timestamp()}: Entorno no compatible con modo {st.session_state.mode}")
                    st.error("Modo del token excede el entorno detectado. Reinicia o usa token inferior.")

# Paso 3: Reproducción con Simulación de Piratería Opcional
if st.session_state.environment_valid and st.session_state.playing:
    with st.expander(f"🔊 Paso 3: Reproducción en Modo {st.session_state.mode}", expanded=st.session_state.step == 3):
        video_url = "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4"
        st.video(video_url, caption="Reproducción simulada (controles restringidos por modo)")
        
        if st.session_state.mode != "Premium":
            st.warning("Modo restringido: Sin pause/rewind para minimizar riesgos.")
        else:
            st.info("Modo Premium: Controles completos disponibles.")
        
        wm_text = f"ID: {st.session_state.watermark_id} | Modo: {st.session_state.mode}"
        frame_img = create_watermark_image(wm_text, st.session_state.mode)
        st.image(frame_img, caption="Preview de Frame con Watermark Forense (invisible en producción)")
        
        st.subheader("Simula Ataques de Piratería (Opcional)")
        col1, col2 = st.columns(2)
        if col1.button("🔌 Simular HDMI Copy Attempt"):
            st.session_state.playing = False
            st.session_state.step = 4
            st.session_state.log.append(f"{timestamp()}: ⚠️ Ataque HDMI detectado. Reproducción detenida.")
            st.error("HDMI no autorizado. Sesión terminada.")
            st.rerun()
        
        if col2.button("📼 Simular Screen Recording"):
            st.session_state.playing = False
            st.session_state.step = 4
            st.session_state.log.append(f"{timestamp()}: ⚠️ Grabación de pantalla detectada. Reproducción detenida.")
            st.error("Grabación detectada. Sesión terminada.")
            st.rerun()
        
        st.metric("Tiempo de Validación Simulado", "0.3s", "Escalable con inversión para cadenas de cine")

# Paso 4: Finalización (si piratería ocurre o playback termina)
if not st.session_state.playing and st.session_state.environment_valid:
    with st.expander("🏁 Paso 4: Sesión Finalizada", expanded=st.session_state.step == 4):
        st.warning("Sesión de reproducción terminada (por piratería simulada o finalización). Revisa los logs abajo.")

# Logs: Siempre visibles al final
st.markdown("---")
st.subheader("📑 Registro de Auditoría (Actualizado en Vivo)")
if st.session_state.log:
    log_text = "\n".join(st.session_state.log)
    st.text_area("Eventos de Sesión:", log_text, height=200)
    st.download_button("📥 Descargar Log", log_text, file_name="visualkey_audit_log.txt")
else:
    st.info("No hay eventos aún. Inicia el flujo.")

# Reinicio global
if st.button("🔄 Reiniciar Flujo Completo"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Sidebar con info para demo
st.sidebar.title("Acerca de VisualKey")
st.sidebar.info("Demo de VisualKey para cadenas de cine: Protección adaptativa para estrenos seguros en casa. Desarrollado por Juan Diego Salas Rueda, Agosto 2025.")
