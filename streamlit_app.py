import streamlit as st
import plotly.graph_objects as go
from engine.hp_engine_reader import HPReader
from engine.hp_engine_manager import HPManager

st.set_page_config(page_title="HP Engine v24.1", layout="wide")

st.title("🏛️ HP Engine v24.1")
st.caption("Saper Vedere: Veriden Stratejik Hükme")

with st.sidebar:
    st.header("Analiz Paneli")
    team = st.text_input("Hedef Takım", "Galatasaray")
    files = st.file_uploader("Veri Enjeksiyonu (CSV/XLSX)", accept_multiple_files=True)
    run_btn = st.button("ANALİZİ MÜHÜRLE")

if run_btn and files:
    # 1. Duyu (Reader)
    data = HPReader().ingest(files)
    # 2. Hüküm (Manager)
    report = HPManager().run_analysis(data, team)
    
    # --- RADAR GRAFİĞİ ---
    FAMILIES = list(report["actual"].keys())
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=[report["expected"].get(k, 0) for k in FAMILIES], theta=FAMILIES, fill="toself", name="DNA (Beklenen)"))
    fig.add_trace(go.Scatterpolar(r=[report["actual"].get(k, 0) for k in FAMILIES], theta=FAMILIES, fill="toself", name="MR (Gerçekleşen)"))
    st.plotly_chart(fig, use_container_width=True)
    
    # --- METRİKLER ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Baskı Şiddeti (PPDA)", report["ppda"])
    c2.metric("Somatotip", f"{report['somatotype']['Endo']}-{report['somatotype']['Meso']}-{report['somatotype']['Ecto']}")
    c3.metric("Kognitif Hız", "Yüksek")
    
    st.info(report["narrative"])
else:
    st.info("Saper Vedere: Analiz için verileri yükleyin ve mühürleyin.")
