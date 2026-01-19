import streamlit as st
import pandas as pd
import json, os, xml.etree.ElementTree as ET
from datetime import datetime

st.set_page_config(page_title="HP Engine Cloud", layout="wide")

st.title("⚽ HP ENGINE – Otonom Futbol Analizi")
st.markdown("**Dual Mode:** Çoklu format okuma + Otomatik JSON normalize")

# ======================
# 1️⃣ Universal Reader
# ======================
def universal_reader(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    try:
        if ext == ".json":
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        elif ext in [".csv", ".tsv"]:
            df = pd.read_csv(file_path)
            return df.to_dict(orient="records")
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(file_path)
            return df.to_dict(orient="records")
        elif ext == ".xml":
            tree = ET.parse(file_path)
            root = tree.getroot()
            return {root.tag: {c.tag: c.text for c in root}}
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return {"text_content": f.read()}
        elif ext == ".html":
            df = pd.read_html(file_path)[0]
            return df.to_dict(orient="records")
        else:
            raise ValueError(f"Desteklenmeyen format: {ext}")
    except Exception as e:
        st.error(f"❌ Okuma hatası: {e}")
        return None

# ======================
# 2️⃣ Analyzer (Core)
# ======================
def run_analysis(file_path):
    data = universal_reader(file_path)
    if not data:
        return None
    # Basit örnek metrikler
    results = {
        "file": os.path.basename(file_path),
        "format": os.path.splitext(file_path)[-1],
        "total_rows": len(data) if isinstance(data, list) else 1,
        "xG_estimate": 1.37,
        "ppda_estimate": 8.3,
        "transition_efficiency": 0.76,
        "timestamp": datetime.now().isoformat()
    }
    # JSON normalize et
    os.makedirs("output", exist_ok=True)
    json_path = f"output/{os.path.basename(file_path)}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    results["normalized_json"] = json_path
    return results

# ======================
# 3️⃣ Streamlit UI
# ======================
uploaded = st.file_uploader(
    "📤 Bir dosya yükle (csv, xlsx, xml, json, txt, html)",
    type=["csv","xlsx","xls","xml","json","txt","html"]
)

if uploaded:
    save_path = f"temp_{uploaded.name}"
    with open(save_path, "wb") as f:
        f.write(uploaded.read())
    st.info(f"Analiz başlatılıyor: {uploaded.name}")
    result = run_analysis(save_path)
    if result:
        st.success("✅ Analiz tamamlandı!")
        st.json(result)
        if os.path.exists(result["normalized_json"]):
            with open(result["normalized_json"], "r", encoding="utf-8") as f:
                data = json.load(f)
            st.subheader("🔍 Normalize edilmiş içerik")
            st.json(data)
else:
    st.warning("Henüz dosya yüklenmedi.")

st.caption("HP Engine Cloud v3.1 – © Hikmet Pınarbaş, 2026")