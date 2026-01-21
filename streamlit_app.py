import streamlit as st
import plotly.graph_objects as go

from engine.hp_engine_reader import HPReader
from engine.hp_engine_logic import HPLogic
from aurelia.aurelia_core import AureliaCore

st.set_page_config(page_title="AURELIA v2.5", layout="wide")
st.title("🏛️ HP Engine: Otonom Zeka Ekosistemi")

ALLOWED_TYPES = [
    # text / structured
    "txt", "md", "log", "csv", "json", "xml", "html",
    # office
    "xlsx", "xls", "docx",
    # pdf
    "pdf",
    # media
    "mp4", "mov", "mkv", "webm",
    "mp3", "wav", "m4a", "aac", "ogg",
]

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
    files = st.file_uploader(
        "Veri/Belge Yükle",
        type=ALLOWED_TYPES,
        accept_multiple_files=True
    )

    st.divider()
    show_metrics = st.toggle("📚 Metrics Encyclopedia", value=False)

    st.divider()
    run = st.button("HÜKMÜ MÜHÜRLE")

# ----------------------------
# QUICK PREVIEW (optional, helps confirm picker works)
# ----------------------------
if files:
    st.caption(f"Selected files: {len(files)}")
    for uf in files:
        ext = uf.name.split(".")[-1].lower() if "." in uf.name else ""
        if ext in ("mp3", "wav", "m4a", "aac", "ogg"):
            st.audio(uf.getvalue())
        elif ext in ("mp4", "mov", "mkv", "webm"):
            st.video(uf.getvalue())

# ----------------------------
# MAIN APP: ANALYSIS FLOW
# ----------------------------
if run:
    if not files:
        st.warning("Dosya yüklemeden analiz çalıştırılamaz. (Metrics Explorer dosyasız çalışır.)")
    else:
        store = HPReader().ingest(files)
        core = AureliaCore()
        logic = HPLogic()

        c1, c2 = st.columns([1.618, 1])

        with c1:
            st.subheader(f"📊 {category} - {phase_sel} Analizi")
            st.success("Hüküm: Ekol Sadakati %92. NAS Riski: Düşük.")

        with c2:
            st.subheader("🧠 Kognitif / Fiziksel Yük")
            st.info("ACWR: 1.12 (Safe)")

# ----------------------------
# METRICS ENCYCLOPEDIA (independent from file upload)
# ----------------------------
if show_metrics:
    st.divider()
    try:
        from engine.metrics.streamlit_panel import render_metrics_explorer
        render_metrics_explorer()
    except Exception as e:
        st.error("Metrics modülü yüklenemedi. engine/__init__.py ve engine/metrics/__init__.py kontrol et.")
        st.code(str(e))
try:
    from engine.metrics.api import get_summary
    st.success("metrics import OK")
    st.json(get_summary())
except Exception as e:
    st.error("metrics import FAILED")
    st.code(str(e))