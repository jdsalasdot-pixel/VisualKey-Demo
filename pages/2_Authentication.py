import streamlit as st
from datetime import datetime
import random

VALID_TOKENS = {
    "premium123": "Premium",
    "standard123": "Standard",
    "compat123": "Compatibility"
}

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generate_watermark_id():
    return ''.join(random.choices('0123456789ABCDEF', k=8))

if st.session_state.adaptive_ready and not st.session_state.token_valid:
    st.title("🎬 VisualKey – Paso 2: Autenticación de Acceso")
    st.info(f"Modo de Entorno Detectado: **{st.session_state.environment}**. Ingresa un token compatible.")
    
    token_input = st.text_input("Ingresa tu token de acceso:", type="password")
    if st.button("Validar y Iniciar Playback"):
        expected_mode = st.session_state.environment
        if token_input in VALID_TOKENS:
            token_mode = VALID_TOKENS[token_input]
            allowed_modes = ["Premium", "Standard", "Compatibility"]
            if allowed_modes.index(token_mode) >= allowed_modes.index(expected_mode):
                st.session_state.token_valid = True
                st.session_state.mode = token_mode
                st.session_state.watermark_id = generate_watermark_id()
                st.session_state.playing = True
                st.session_state.log.append(f"{timestamp()}: Token válido '{token_input}' aceptado para modo {token_mode}")
                st.session_state.log.append(f"{timestamp()}: ID de Watermark generado = {st.session_state.watermark_id}")
                st.success("Acceso concedido. Procede a Playback.")
            else:
                st.error("Nivel de token excede el entorno permitido. Usa un token de nivel inferior.")
        else:
            st.session_state.log.append(f"{timestamp()}: Intento de token inválido – {token_input}")
            st.error("Token inválido. Intenta nuevamente.")
