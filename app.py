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
st.sidebar.info("Prototype for audiovisual content protection. Sequential flow: Environment Scan → Token Validation → Secure Playback → Optional Piracy Simulation → Logs.")
st.sidebar.markdown("Developed by Juan Diego Salas Rueda, August 2025.")

# Main title
st.title("🎬 VisualKey – Adaptive Secure Playback Prototype")

# Step 1: Environment Scan (always first)
with st.expander("🔍 Step 1: Initial Device Environment Scan", expanded=not st.session_state.adaptive_ready):
    if not st.session_state.adaptive_ready:
        option = st.selectbox("Select simulated environment:", [
            "Verified Secure Device (e.g., registered home system)",
            "Trusted Home Wi-Fi",
            "VPN / Unknown Network"
        ])
        if st.button("Run Environment Scan"):
            if "Secure" in option:
                st.session_state.environment = "Premium"
            elif "Home" in option:
                st.session_state.environment = "Standard"
            else:
                st.session_state.environment = "Compatibility"
            st.session_state.adaptive_ready = True
            st.session_state.log.append(f"{timestamp()}: Environment detected → {st.session_state.environment}")
            st.success(f"Environment detected: **{st.session_state.environment}**. Proceed to authentication.")
            st.rerun()

# Step 2: Token Validation (after environment)
if st.session_state.adaptive_ready and not st.session_state.token_valid:
    with st.expander("🔐 Step 2: Access Authentication", expanded=True):
        st.info(f"Detected Environment Mode: **{st.session_state.environment}**. Enter a compatible or lower token.")
        token_input = st.text_input("Enter your access token:", type="password")
        if st.button("Validate and Start Playback"):
            expected_mode = st.session_state.environment
            if token_input.strip() == "":
                st.warning("Enter a valid token.")
            elif token_input in VALID_TOKENS:
                token_mode = VALID_TOKENS[token_input]
                allowed_modes = ["Premium", "Standard", "Compatibility"]
                if allowed_modes.index(token_mode) >= allowed_modes.index(expected_mode):
                    st.session_state.token_valid = True
                    st.session_state.mode = token_mode
                    st.session_state.watermark_id = generate_watermark_id()
                    st.session_state.playing = True
                    st.session_state.log.append(f"{timestamp()}: Valid token '{token_input}' accepted for mode {token_mode}")
                    st.session_state.log.append(f"{timestamp()}: Watermark ID generated = {st.session_state.watermark_id}")
                    st.success("Access granted. Starting playback.")
                    st.rerun()
                else:
                    st.error("Token level exceeds allowed environment. Use a lower token.")
            else:
                st.session_state.log.append(f"{timestamp()}: Invalid token attempt – {token_input}")
                st.error("Invalid token. Try again.")

# Step 3: Playback Session (with optional piracy simulation)
if st.session_state.token_valid and st.session_state.playing and st.session_state.mode:
    with st.expander(f"🔊 Step 3: Playback in {st.session_state.mode} Mode", expanded=True):
        # Simulated video
        video_url = "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4"  # Short public test video
        st.video(video_url)
        st.caption("Simulated playback of protected content")
        
        # Watermark preview
        wm_text = f"ID: {st.session_state.watermark_id}"
        frame_img = create_watermark_image(wm_text, st.session_state.mode)
        st.image(frame_img, caption="Forensic Watermark Preview (invisible in real production)", use_column_width=True)
        
        # Optional piracy simulation
        st.subheader("Simulate Piracy Attacks (Optional)")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔌 Simulate HDMI Copy Attempt"):
                st.session_state.playing = False
                st.session_state.log.append(f"{timestamp()}: ⚠️ HDMI attack detected. Playback stopped.")
                st.error("Unauthorized HDMI output. Session terminated.")
                st.rerun()
        with col2:
            if st.button("📼 Simulate Screen Recording"):
                st.session_state.playing = False
                st.session_state.log.append(f"{timestamp()}: ⚠️ Screen recorder detected. Playback stopped.")
                st.error("Recording detected. Session terminated.")
                st.rerun()
        
        # Mock metrics for professional demo
        st.metric("Simulated Validation Time", "0.3 sec", "Scalable to millions of sessions with investment")

# Final Step: If playback ends
if st.session_state.token_valid and not st.session_state.playing:
    with st.expander("🏁 Session Ended", expanded=True):
        st.warning("Playback session ended. Check logs below.")
        if st.button("Reset Application"):
            for key in ['adaptive_ready', 'environment', 'token_valid', 'playing', 'mode', 'watermark_id']:
                st.session_state[key] = False if key in ['adaptive_ready', 'token_valid', 'playing'] else None
            st.session_state.log = []  # Clear logs for full reset
            st.rerun()

# Audit Log: Always at the end, live updated
st.markdown("---")
st.subheader("📑 Audit Log")
if st.session_state.log:
    log_text = "\n".join(st.session_state.log)
    st.text_area("Session Events:", log_text, height=200)
    st.download_button("📥 Download Log", log_text.encode('utf-8'), file_name="visualkey_audit_log.txt")
else:
    st.info("No events logged yet. Start the flow.")
