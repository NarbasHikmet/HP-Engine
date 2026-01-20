import streamlit as st
from engine.hp_engine_reader import HPReader
from engine.hp_engine_logic import HPLogic
from engine.hp_engine_vision import HPVision

st.set_page_config(page_title="HP Engine v24.1", layout="wide")
st.title("🏛️ HP Engine: AURELIA Master System")

with st.sidebar:
    st.header("1. Ana Analiz Modülü")
    mode = st.selectbox("Kategori Seçiniz", [
        "Pre-Match Analysis", "Post-Match Analysis", "Individual Analysis",
        "Team Tactical Analysis", "Seasonal & Tournament Analysis",
        "Team Squad Engineering Analysis", "General Analysis"
    ])

    st.header("2. Yardımcı Modüller")
    v1 = st.checkbox("Video Analysis Analysis")
    v2 = st.checkbox("Body Position and Orientation Analysis")
    v3 = st.checkbox("Positional Analysis Analysis")

    st.header("3. Veri Girişi")
    files = st.file_uploader("Metrik/Belge Yükle (CSV, PDF, XML...)", accept_multiple_files=True)
    videos = st.file_uploader("Video Yükle (MP4)", type=["mp4"], accept_multiple_files=True)
    
    run = st.button("ANALİZİ MÜHÜRLE")

if run and files:
    # 1. Veri Okuma
    reader = HPReader()
    store = reader.ingest(files)
    
    # 2. Ana Analiz Seçimi
    logic = HPLogic()
    if mode == "Pre-Match Analysis": res = logic.run_pre_match_analysis(store)
    elif mode == "Post-Match Analysis": res = logic.run_post_match_analysis(store)
    # ... Diğer modüller buraya eklenecek
    
    st.success(f"Ana Modül: {mode} aktif.")
    st.write(res)
    
    # 3. Yardımcı Modüller (Seçilirse)
    vision = HPVision()
    if v1 and videos: st.info(vision.video_analysis_analysis(videos))
    if v2: st.info(vision.body_position_orientation_rotation_analysis(store))
    if v3: st.info(vision.positional_analysis_analysis(store))
