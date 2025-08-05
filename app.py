import streamlit as st
from datetime import datetime
import random
from PIL import Image, ImageDraw, ImageFont

# Token-to-environment mapping
VALID_TOKENS = {
    "premium123": "Premium",
    "standard123": "Standard",
    "compat123": "Compatibility"
}

# Initialize session state
for key in ['adaptive_ready', 'environment', 'token_valid', 'playing', 'mode', 'watermark_id', 'log']:
    if key not in st.session_state:
        if key == 'log':
            st.session_state[key] = []
        elif key in ['adaptive_ready', 'token_valid', 'playing']:
            st.session_state[key] = False
        else:
            st.session_state[key] = None

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
    
    if mode == 'Compatibility':
        text_color = (255, 0, 0)
        x = (img.width - text_width) // 2
        y = (img.height - text_height) // 2
    else:
        text_color = (150, 150, 150)
        x = img.width - text_width - 10
        y = img.height - text_height - 10
    
    draw.text((x, y), wm_text, font=font, fill=text_color)
    return img

# App configuration
st.set_page_config(page_title="VisualKey Prototype", page_icon="🎬", layout="wide")

# Sidebar for demo info
st.sidebar.title("VisualKey Demo")
st.sidebar.info("Prototipo para protección de contenido audiovisual. Flujo secuencial: Escaneo de entorno → Validación de token → Reproducción segura → Simulación de piratería (opcional) → Logs.")
st.sidebar.markdown("Desarrollado por Juan Diego Salas Rueda, Agosto 2025.")

# Main title
st.title("🎬 VisualKey – Prototipo de Playback Seguro Adaptativo")

# Paso 1: Escaneo de Entorno (siempre primero)
with st.expander("🔍 Paso 1: Escaneo Inicial de Entorno del Dispositivo", expanded=not st.session_state.adaptive_ready):
    if not st.session_state.adaptive_ready:
        option = st.selectbox("Selecciona entorno simulado:", [
            "Dispositivo Seguro Verificado (e.g., sistema registrado en casa)",
            "Wi-Fi Hogar Confiable",
            "VPN / Red Desconocida"
        ])
        if st.button("Ejecutar Escaneo de Entorno"):
            if "Seguro" in option:
                st.session_state.environment = "Premium"
            elif "Hogar" in option:
                st.session_state.environment = "Standard"
            else:
                st.session_state.environment = "Compatibility"
            st.session_state.adaptive_ready = True
            st.session_state.log.append(f"{timestamp()}: Entorno detectado → {st.session_state.environment}")
            st.success(f"Entorno detectado: **{st.session_state.environment}**. Procede a autenticación.")
            st.rerun()

# Paso 2: Validación de Token (después del entorno)
if st.session_state.adaptive_ready and not st.session_state.token_valid:
    with st.expander("🔐 Paso 2: Autenticación de Acceso", expanded=True):
        st.info(f"Modo de Entorno Detectado: **{st.session_state.environment}**. Ingresa un token compatible o inferior.")
        token_input = st.text_input("Ingresa tu token de acceso:", type="password")
        if st.button("Validar e Iniciar Reproducción"):
            expected_mode = st.session_state.environment
            if token_input.strip() == "":
                st.warning("Ingresa un token válido.")
            elif token_input in VALID_TOKENS:
                token_mode = VALID_TOKENS[token_input]
                allowed_modes = ["Premium", "Standard", "Compatibility"]
                if allowed_modes.index(token_mode) >= allowed_modes.index(expected_mode):
                    st.session_state.token_valid = True
                    st.session_state.mode = token_mode
                    st.session_state.watermark_id = generate_watermark_id()
                    st.session_state.playing = True
                    st.session_state.log.append(f"{timestamp()}: Token válido '{token_input}' aceptado para modo {token_mode}")
                    st.session_state.log.append(f"{timestamp()}: ID de Watermark generado = {st.session_state.watermark_id}")
                    st.success("Acceso concedido. Iniciando reproducción.")
                    st.rerun()
                else:
                    st.error("Nivel de token excede el entorno permitido. Usa un token inferior.")
            else:
                st.session_state.log.append(f"{timestamp()}: Intento de token inválido – {token_input}")
                st.error("Token inválido. Intenta nuevamente.")

# Paso 3: Sesión de Reproducción (con simulación de piratería opcional)
if st.session_state.token_valid and st.session_state.playing and st.session_state.mode:
    with st.expander(f"🔊 Paso 3: Reproducción en Modo {st.session_state.mode}", expanded=True):
        # Simulación de video
        video_url = "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4"  # Video de prueba corto y público
        st.video(video_url, caption="Reproducción simulada del contenido protegido")
        
        # Preview de watermark
        wm_text = f"ID: {st.session_state.watermark_id}"
        frame_img = create_watermark_image(wm_text, st.session_state.mode)
        st.image(frame_img, caption="Vista Previa de Watermark Forense (invisible en producción real)", use_column_width=True)
        
        # Simulación de piratería opcional
        st.subheader("Simula Ataques de Piratería (Opcional)")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔌 Simular Intento de Copia HDMI"):
                st.session_state.playing = False
                st.session_state.log.append(f"{timestamp()}: ⚠️ Ataque HDMI detectado. Reproducción detenida.")
                st.error("Salida HDMI no autorizada. Sesión terminada.")
                st.rerun()
        with col2:
            if st.button("📼 Simular Grabación de Pantalla"):
                st.session_state.playing = False
                st.session_state.log.append(f"{timestamp()}: ⚠️ Grabador de pantalla detectado. Reproducción detenida.")
                st.error("Grabación detectada. Sesión terminada.")
                st.rerun()
        
        # Métricas mock para demo profesional
        st.metric("Tiempo de Validación Simulado", "0.3 seg", "Escalable a millones de sesiones con inversión")

# Paso Final: Si reproducción termina
if st.session_state.token_valid and not st.session_state.playing:
    with st.expander("🏁 Sesión Finalizada", expanded=True):
        st.warning("Sesión de reproducción terminada. Revisa los logs abajo.")
        if st.button("Reiniciar Aplicación"):
            for key in ['adaptive_ready', 'environment', 'token_valid', 'playing', 'mode', 'watermark_id']:
                st.session_state[key] = False if key in ['adaptive_ready', 'token_valid', 'playing'] else None
            st.session_state.log = []  # Limpiar logs para reinicio completo
            st.rerun()

# Audit Log: Siempre al final, actualizado en vivo
st.markdown("---")
st.subheader("📑 Registro de Auditoría")
if st.session_state.log:
    log_text = "\n".join(st.session_state.log)
    st.text_area("Eventos de Sesión:", log_text, height=200)
    st.download_button("📥 Descargar Log", log_text.encode('utf-8'), file_name="visualkey_audit_log.txt")
else:
    st.info("No hay eventos registrados aún. Inicia el flujo.")
