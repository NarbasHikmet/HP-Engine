# engine/app.py
import streamlit as st
from engine.hp_engine_core import run_analysis
import os, json
from datetime import datetime

st.set_page_config(page_title="HP Engine Cloud", layout="wide")

st.title("⚽ HP ENGINE – Dual Data Mode")
st.markdown("Yapay zekâ destekli futbol analizi • Çoklu dosya formatı desteği (CSV, XLSX, XML, TXT, DOCX, JSON, HTML)")

uploaded = st.file_uploader("📤 Bir dosya yükle", type=["csv","xlsx","xls","xml","json","txt","docx","html"])
if uploaded:
    save_path = f"temp_{uploaded.name}"
    with open(save_path, "wb") as f:
        f.write(uploaded.read())

    st.info(f"Analiz başlatılıyor: {uploaded.name}")
    result = run_analysis(save_path)
    
    if result:
        st.success("✅ Analiz tamamlandı!")
        st.json(result)
        if os.path.exists(result["saved_json"]):
            with open(result["saved_json"], "r", encoding="utf-8") as f:
                data = json.load(f)
            st.subheader("🔍 JSON içeriği (normalize edilmiş)")
            st.json(data)
else:
    st.warning("Henüz dosya yüklenmedi.")

st.caption("HP Engine Cloud v3.0 © Hikmet Pınarbaş 2026")