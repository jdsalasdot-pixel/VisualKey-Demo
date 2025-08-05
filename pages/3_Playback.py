import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

@st.cache_data
def create_watermark_image(wm_text, mode):
    img = Image.new("RGB", (640, 360), color=(20, 20, 20))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    text_color = (255, 0, 0) if mode == 'Compatibility' else (150, 150, 150)
    draw.text((10, 10), wm_text, font=font, fill=text_color)
    return img

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if st.session_state.token_valid and st.session_state.playing:
    st.title("🎬 VisualKey – Paso 3: Sesión de Playback")
    st.subheader(f"Modo Activo: {st.session_state.mode}")
    
    # Simulación de video (usa URL pública; agrega a assets/ si local)
    video_url = "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4"  # Video de prueba corto
    st.video(video_url)
    
    wm_text = f"ID: {st.session_state.watermark_id}"
    frame_img = create_watermark_image(wm_text, st.session_state.mode)
    st.image(frame_img, caption="Vista Previa de Frame con Watermark Forense")
    
    col1, col2 = st.columns(2)
    if col1.button("🔌 Simular HDMI Copy Attempt"):
        st.session_state.playing = False
        st.session_state.log.append(f"{timestamp()}: ⚠️ HDMI attack detected. Playback stopped.")
        st.error("HDMI output unauthorized. Session terminated.")
    
    if col2.button("📼 Simular Screen Recording"):
        st.session_state.playing = False
        st.session_state.log.append(f"{timestamp()}: ⚠️ Screen recorder detected. Playback stopped.")
        st.error("Screen recording detected. Session terminated.")
    
    if not st.session_state.playing:
        st.warning("🔒 Playback session ended.")
        if st.button("Restart Application"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
