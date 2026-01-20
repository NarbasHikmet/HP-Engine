import streamlit as st
import plotly.graph_objects as go
from engine.hp_engine_reader import HPReader
from engine.hp_engine_logic import HPLogic

st.set_page_config(page_title="AURELIA v2.5", layout="wide")
st.title("🏛️ HP Engine: Otonom Zeka Ekosistemi")

with st.sidebar:
    st.header("SAPER VEDERE")
    mode = st.selectbox("Analiz Kategorisi", [
        "Pre-Match Analysis", "Post-Match Analysis", "Individual Analysis",
        "Team Tactical Analysis", "Seasonal Analysis", "Squad Engineering", "General Analysis"
    ])
    st.subheader("Yardımcı Katmanlar")
    v1 = st.checkbox("YOLO11 Pose & Scanning")
    v2 = st.checkbox("Vücut Oryantasyonu (Body Pos)")
    
    files = st.file_uploader("Veri Enjeksiyonu (CSV, PDF, XML...)", accept_multiple_files=True)
    run = st.button("HÜKMÜ MÜHÜRLE")

if run and files:
    store = HPReader().ingest(files)
    logic = HPLogic()
    result = logic.analyze_phase_logic(store, mode)
    
    # Dashboard: Altın Oran Yerleşimi
    c1, c2 = st.columns([1.618, 1])
    with c1:
        st.subheader(f"📊 {mode} Çıktısı")
        st.write(result)
        # xT Grid Görselleştirme
        xt_data = logic.ana.calculate_xt(store["data"])
        fig = go.Figure(data=go.Heatmap(z=xt_data, colorscale='Viridis'))
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.subheader("🧠 Kognitif Denetim (NAS)")
        nas = logic.ana.detect_nas(store["data"])
        if nas: st.error(f"Kritik NAS Tespit Edildi: {len(nas)} Sekans")
        else: st.success("Kognitif Stabilite: Yüksek")
