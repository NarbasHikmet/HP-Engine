import streamlit as st
from engine.hp_engine_reader import HPReader
from engine.hp_engine_manager import HPManager

st.set_page_config(page_title="HP Engine v24.1", layout="wide")

st.title("🏛️ HP Engine: AURELIA Master System")

with st.sidebar:
    st.header("1. Analiz Kategorisi")
    analysis_mode = st.selectbox("Seçiniz", [
        "Pre-Match Analysis", "Post-Match Analysis", "Individual Analysis",
        "Team Tactical Analysis", "Seasonal & Tournament Analysis",
        "Team Squad Engineering Analysis", "General Analysis"
    ])

    st.header("2. Yardımcı Modüller (Opsiyonel)")
    use_video = st.checkbox("Video Analysis Analysis")
    use_body = st.checkbox("Body Position and Orientation Analysis")
    use_positional = st.checkbox("Positional Analysis Analysis")

    st.header("3. Veri Enjeksiyonu")
    files = st.file_uploader("Multi-Format (CSV, PDF, XML...)", accept_multiple_files=True)
    video_files = st.file_uploader("MP4 Video Klipleri", type=["mp4"], accept_multiple_files=True)
    
    run_btn = st.button("SAPER VEDERE: ANALİZİ MÜHÜRLE")

if run_btn and files:
    # Master Manager'a tüm tercihleri gönderiyoruz
    manager = HPManager()
    results = manager.run_hybrid_analysis(
        files=files, 
        videos=video_files if use_video else None,
        mode=analysis_mode,
        helpers={"body": use_body, "positional": use_positional}
    )
    # Sonuçların görselleştirilmesi...
