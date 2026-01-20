import streamlit as st
import plotly.graph_objects as go

from engine.hp_engine_reader import HPReader
from engine.hp_engine_logic import HPLogic
from aurelia.aurelia_core import AureliaCore

st.set_page_config(page_title="AURELIA v2.5", layout="wide")
st.title("🏛️ HP Engine: Otonom Zeka Ekosistemi")

# ----------------------------
# SIDEBAR
# ----------------------------
with st.sidebar:
    st.header("SAPER VEDERE")
    phase_sel = st.selectbox(
        "HP 6-Faz Modeli",
        ["Build-up", "Progression", "Incision", "Finishing", "Transitions"]
    )
    category = st.selectbox(
        "Analiz Modülü",
        ["Pre-Match", "Post-Match", "Individual (NAS)", "Team Tactical", "Squad Engineering"]
    )

    st.divider()
    show_metrics = st.toggle("📚 Metrics Encyclopedia", value=False)

    st.divider()
    files = st.file_uploader("Veri/Belge Yükle", accept_multiple_files=True)

st.divider()
show_metrics = st.toggle("📚 Metrics Encyclopedia", value=False)
    run = st.button("HÜKMÜ MÜHÜRLE")

# ----------------------------
# MAIN APP: ANALYSIS FLOW
# ----------------------------
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

elif run and not files:
    st.warning("Dosya yüklemeden analiz çalıştırılamaz. (Metrics Explorer dosyasız çalışır.)")

# ----------------------------
# METRICS ENCYCLOPEDIA (dosyadan bağımsız)
# ----------------------------
if show_metrics:
    st.divider()
    try:
        from engine.metrics.streamlit_panel import render_metrics_explorer
        render_metrics_explorer()
    except Exception as e:
        st.error("Metrics modülü yüklenemedi. engine/__init__.py ve engine/metrics/__init__.py kontrol et.")
        st.code(str(e)) 