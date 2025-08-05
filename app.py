import streamlit as st
from datetime import datetime
import random
from PIL import Image, ImageDraw, ImageFont

# Token-to-environment mapping (ajustado para flujo: token primero, entorno después)
VALID_TOKENS = {
    "premium123": "Premium",
    "standard123": "Standard",
    "compat123": "Compatibility"
}

# Inicializar session_state
for key in ['token_valid', 'environment_valid', 'playing', 'mode', 'watermark_id', 'log']:
    if key not in st.session_state:
        if key == 'log':
            st.session_state[key] = []
        elif key in ['token_valid', 'environment_valid', 'playing']:
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

    text_color = (255, 0, 0) if mode == 'Compatibility' else (150, 150, 150)
    x = (img.width - text_width) // 2 if mode == 'Compatibility' else img.width - text_width - 10
    y = (img.height - text_height) // 2 if mode == 'Compatibility' else img.height - text_height - 10

    draw.text((x, y), wm_text, font=font, fill=text_color)
    return img

# Configuración de la app
st.set_page_config(page_title="VisualKey Demo", page_icon="🎬", layout="wide")
st.title("🎬 VisualKey – Prototipo de Playback Seguro Adaptativo")
st.info("Flujo secuencial: Ingresa token → Valida entorno → Reproduce → Simula piratería (opcional) → Revisa logs.")

# Paso 1: Validación de Token (primero, como pediste)
if not st.session_state.token_valid:
    st.subheader("🔐 Paso 1: Autenticación de Acceso")
    token_input = st.text_input("Ingresa tu token de acceso:", type="password")
    if st.button("Validar Token"):
        if token_input in VALID_TOKENS:
            st.session_state.mode = VALID_TOKENS[token_input]
            st.session_state.token_valid = True
            st.session_state.log.append(f"{timestamp()}: Token válido '{token_input}' aceptado para modo tentativo {st.session_state.mode}")
            st.success("Token validado. Procede a validar el entorno.")
            st.rerun()  # Refresca para mostrar el siguiente paso
        else:
            st.session_state.log.append(f"{timestamp()}: Intento de token inválido – {token_input}")
            st.error("Token inválido. Intenta nuevamente.")

# Paso 2: Validación del Entorno (después del token)
if st.session_state.token_valid and not st.session_state.environment_valid:
    st.subheader("🔍 Paso 2: Escaneo de Entorno del Dispositivo")
    option = st.selectbox("Selecciona entorno simulado:", [
        "Dispositivo Seguro Verificado (Premium)",
        "Red Hogar Confiable (Standard)",
        "VPN / Red Desconocida (Compatibility)"
    ])
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
            st.session_state.log.append(f"{timestamp()}: Entorno validado como {environment}. Modo final: {st.session_state.mode}")
            st.session_state.log.append(f"{timestamp()}: Watermark ID generado = {st.session_state.watermark_id}")
            st.success("Entorno seguro. Iniciando reproducción.")
            st.rerun()
        else:
            st.error("Modo del token excede el entorno detectado. Reinicia o usa token inferior.")
            st.session_state.log.append(f"{timestamp()}: Entorno no compatible con modo {st.session_state.mode}")

# Paso 3: Reproducción (con simulación de piratería opcional)
if st.session_state.environment_valid and st.session_state.playing:
    st.subheader(f"🔊 Paso 3: Reproducción en Modo {st.session_state.mode}")
    
    # Embed de video simulado
    video_url = "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4"  # Video corto de prueba
    st.video(video_url, caption="Reproducción simulada (controles restringidos por modo)")
    
    if st.session_state.mode != "Premium":
        st.warning("Modo restringido: Sin pause/rewind para minimizar riesgos.")
    
    # Preview de watermark
    wm_text = f"ID: {st.session_state.watermark_id} | Modo: {st.session_state.mode}"
    frame_img = create_watermark_image(wm_text, st.session_state.mode)
    st.image(frame_img, caption="Preview de Frame con Watermark Forense (invisible en producción)")
    
    # Simulación de piratería (opcional)
    st.subheader("Simula Ataques de Piratería (Opcional)")
    col1, col2 = st.columns(2)
    if col1.button("🔌 Simular HDMI Copy Attempt"):
        st.session_state.playing = False
        st.session_state.log.append(f"{timestamp()}: ⚠️ Ataque HDMI detectado. Reproducción detenida.")
        st.error("HDMI no autorizado. Sesión terminada.")
        st.rerun()
    
    if col2.button("📼 Simular Screen Recording"):
        st.session_state.playing = False
        st.session_state.log.append(f"{timestamp()}: ⚠️ Grabación de pantalla detectada. Reproducción detenida.")
        st.error("Grabación detectada. Sesión terminada.")
        st.rerun()
    
    # Métrica mock para demo
    st.metric("Tiempo de Validación Simulado", "0.3s", "Escalable con inversión")

# Logs: Siempre al final, registrando todo
st.markdown("---")
st.subheader("📑 Registro de Auditoría (Actualizado en Vivo)")
if st.session_state.log:
    log_text = "\n".join(st.session_state.log)
    st.text_area("Eventos de Sesión:", log_text, height=200)
    st.download_button("📥 Descargar Log", log_text, file_name="visualkey_audit_log.txt")
else:
    st.info("No hay eventos aún. Inicia el flujo.")

# Botón de reinicio global
if st.button("🔄 Reiniciar Flujo Completo"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
