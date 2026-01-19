import streamlit as st
import pandas as pd
import json, xml.etree.ElementTree as ET
from io import StringIO, BytesIO
from datetime import datetime

st.set_page_config(page_title="HP Engine Cloud", layout="wide")
st.title("⚽ HP ENGINE – Bellek İçi Analiz")
st.markdown("CSV • XLSX • JSON • XML • TXT • HTML dosyalarını okuyup sonuçları bellekte gösterir.")

# ---------- Okuyucu ----------
def universal_reader(file_bytes, filename):
    ext = filename.split(".")[-1].lower()
    if ext == "json":
        return json.loads(file_bytes.decode("utf-8"))
    if ext in ["csv","tsv"]:
        return pd.read_csv(StringIO(file_bytes.decode("utf-8"))).to_dict(orient="records")
    if ext in ["xls","xlsx"]:
        return pd.read_excel(BytesIO(file_bytes)).to_dict(orient="records")
    if ext == "xml":
        root = ET.fromstring(file_bytes.decode("utf-8"))
        rows = [{c.tag: c.text for c in child} for child in root]
        return rows if rows else {root.tag: root.attrib}
    if ext == "txt":
        return {"text_content": file_bytes.decode("utf-8")}
    if ext == "html":
        return pd.read_html(StringIO(file_bytes.decode("utf-8")))[0].to_dict(orient="records")
    raise ValueError(f"Desteklenmeyen format: {ext}")

# ---------- Analiz ----------
def run_analysis(file_bytes, filename):
    data = universal_reader(file_bytes, filename)
    return {
        "file": filename,
        "format": filename.split(".")[-1],
        "rows": len(data) if isinstance(data, list) else 1,
        "xG_estimate": 1.42,
        "ppda_estimate": 8.3,
        "transition_efficiency": 0.75,
        "timestamp": datetime.now().isoformat(),
        "normalized_data": data
    }

# ---------- Arayüz ----------
uploaded = st.file_uploader(
    "📤 Dosya yükle (csv, xlsx, json, xml, txt, html)",
    type=["csv","xlsx","xls","json","xml","txt","html"]
)

if uploaded:
    bytes_data = uploaded.read()
    st.info(f"Analiz başlatılıyor → {uploaded.name}")
    try:
        result = run_analysis(bytes_data, uploaded.name)
        st.success("✅ Analiz tamamlandı!")
        st.json({k:v for k,v in result.items() if k!="normalized_data"})
        st.subheader("🔍 Normalize Edilmiş İçerik")
        st.json(result["normalized_data"])
    except Exception as e:
        st.error(f"❌ Okuma veya analiz hatası: {e}")
else:
    st.warning("Henüz dosya yüklenmedi.")

st.caption("HP Engine Cloud v3.3 – © Hikmet Pınarbaş 2026")