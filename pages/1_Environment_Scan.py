import streamlit as st
from datetime import datetime

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

st.title("🎬 VisualKey – Paso 1: Escaneo de Entorno Inicial")

if not st.session_state.adaptive_ready:
    st.subheader("🔍 Detección Simulada de Dispositivo/Red")
    st.info("Selecciona un entorno para simular compatibilidad (basado en hardware/red real en producción).")
    
    option = st.selectbox("Entorno simulado:", [
        "Dispositivo Seguro Verificado (e.g., sistema certificado para Premium)",
        "Red Hogar Confiable (e.g., Wi-Fi estándar)",
        "VPN / Red Desconocida (e.g., bajo compatibilidad)"
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
        st.success(f"Entorno detectado: **{st.session_state.environment}**. Procede a Autenticación.")
