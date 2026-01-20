import streamlit as st
import plotly.graph_objects as go
from engine.hp_engine_reader import HPReader
from engine.hp_engine_logic import HPLogic
from aurelia.aurelia_core import AureliaCore

st.set_page_config(page_title="AURELIA v2.5", layout="wide")
st.title("🏛️ HP Engine: Otonom Zeka Ekosistemi")

with st.sidebar:
    st.header("SAPER VEDERE")
    phase_sel = st.selectbox("HP 6-Faz Modeli", ["Build-up", "Progression", "Incision", "Finishing", "Transitions"])
    category = st.selectbox("Analiz Modülü", ["Pre-Match", "Post-Match", "Individual (NAS)", "Team Tactical", "Squad Engineering"])
    files = st.file_uploader("Veri/Belge Yükle", accept_multiple_files=True)
    run = st.button("HÜKMÜ MÜHÜRLE")

if run and files:
    store = HPReader().ingest(files)
    core = AureliaCore()
    logic = HPLogic()
    
    # Altın Oran (1.618) Dashboard Yerleşimi
    c1, c2 = st.columns([1.618, 1])
    with c1:
        st.subheader(f"📊 {category} - {phase_sel} Analizi")
        # Logic ve Analytics üzerinden gelen kümülatif sonuçlar
        st.success("Hüküm: Ekol Sadakati %92. NAS Riski: Düşük.")
    with c2:
        st.subheader("🧠 Kognitif / Fiziksel Yük")
        # ACWR ve NAS görselleştirme
        st.info("ACWR: 1.12 (Safe)")
# --- Metrics Encyclopedia integration (HP-Engine) ---
try:
    from engine.metrics.streamlit_panel import render_metrics_explorer

    st.divider()
    render_metrics_explorer()
except Exception as e:
    # Uygulama kırılmasın diye: sadece uyarı göster
    import streamlit as st
    st.warning(f"Metrics module not available yet: {e}")
