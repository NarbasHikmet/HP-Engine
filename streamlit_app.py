import streamlit as st
from engine.hp_engine_reader import HPReader
from engine.hp_engine_logic import HPLogic

st.set_page_config(page_title="AURELIA v2.5", layout="wide")
st.title("🏛️ HP Engine: Otonom Zeka Ekosistemi")

with st.sidebar:
    st.header("1. HİKMET PINARBAŞI 6-FAZ MODELİ")
    phase = st.selectbox("Faz", ["Build-up", "Progression", "Incision", "Finishing", "Transitions"])
    st.header("2. ANALİZ KATEGORİSİ (7 MODÜL)")
    category = st.selectbox("Modül", ["Pre-Match", "Post-Match", "Individual (NAS)", "Team Tactical", "Squad Engineering", "Seasonal", "General"])
    st.header("3. VİZYON KATMANLARI")
    yolo_active = st.checkbox("YOLO11 Pose & Scanning")
    
    files = st.file_uploader("Veri/Belge Yükle (CSV, PDF, XML, DOCX)", accept_multiple_files=True)
    run = st.button("HÜKMÜ MÜHÜRLE")

if run and files:
    store = HPReader().ingest(files)
    result = HPLogic().run_comprehensive_analysis(store, category)
    st.success(f"Analiz Fazı: {phase} | Kategori: {category} Mühürlendi.")
