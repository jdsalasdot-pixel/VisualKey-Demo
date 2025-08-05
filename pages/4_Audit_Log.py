import streamlit as st

st.title("🎬 VisualKey – Paso 4: Registro de Auditoría")

if st.session_state.log:
    log_text = "\n".join(st.session_state.log)
    st.text_area("Eventos de Sesión:", log_text, height=200)
    st.download_button("📥 Descargar Log", log_text, file_name="visualkey_audit_log.txt")
else:
    st.info("No hay eventos registrados aún. Completa los pasos anteriores.")
