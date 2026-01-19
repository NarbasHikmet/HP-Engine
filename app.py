import streamlit as st
import json, os, time
from datetime import datetime

st.set_page_config(page_title="HP Engine Cloud", layout="wide")

st.title("⚽ HP ENGINE – Otonom Futbol Analizi")
st.markdown("Yapay zeka destekli, veri odaklı pre-match ve post-match analiz sistemi (mobil uyumlu).")

# Upload area
uploaded_file = st.file_uploader("📤 Maç veya analiz dosyasını yükle (.json / .csv)", type=["json", "csv"])

if uploaded_file:
    st.info(f"Dosya alındı: **{uploaded_file.name}**")

    # Geçici olarak yükle
    save_path = f"temp_{uploaded_file.name}"
    with open(save_path, "wb") as f:
        f.write(uploaded_file.read())

    # Basit örnek analiz
    results = {
        "file": uploaded_file.name,
        "xG": 1.42,
        "PPDA": 7.9,
        "Transition Efficiency": 0.78,
        "Team Compactness": 0.66,
        "Neuro-Score": 91.4,
        "Processed": datetime.now().isoformat()
    }

    st.success("Analiz tamamlandı ✅")
    st.json(results)

    # Save results
    os.makedirs("output", exist_ok=True)
    with open(f"output/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
        json.dump(results, f, indent=4)

    # Basit görselleştirme
    st.subheader("📊 Hızlı Görselleştirme")
    st.bar_chart({
        "Metrics": [results["xG"], results["PPDA"], results["Transition Efficiency"], results["Team Compactness"]],
    })
else:
    st.warning("Lütfen bir maç dosyası yükle (örnek: test_match.json).")

st.markdown("---")
st.caption("HP Engine Cloud © 2026 — Designed by Hikmet Pınarbaş")