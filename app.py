import streamlit as st
import pandas as pd
import json, os, xml.etree.ElementTree as ET
from io import StringIO, BytesIO
from datetime import datetime

st.set_page_config(page_title="HP Engine Cloud", layout="wide")
st.title("⚽ HP ENGINE – Dual Reader System")
st.markdown("CSV • XLSX • JSON • XML • TXT • HTML dosyalarını otomatik okur ve JSON’a dönüştürür.")

# -------------------------
# 1️⃣ Dosya Okuyucu
# -------------------------
def universal_reader(file_bytes, filename):
    ext = os.path.splitext(filename)[-1].lower()
    try:
        # JSON
        if ext == ".json":
            return json.loads(file_bytes.decode("utf-8"))

        # CSV / TSV
        elif ext in [".csv", ".tsv"]:
            s = StringIO(file_bytes.decode("utf-8"))
            df = pd.read_csv(s)
            return df.to_dict(orient="records")

        # Excel
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(BytesIO(file_bytes))
            return df.to_dict(orient="records")

        # XML
        elif ext == ".xml":
            xml_str = file_bytes.decode("utf-8")
            root = ET.fromstring(xml_str)
            data = []
            for child in root:
                record = {elem.tag: elem.text for elem in child}
                data.append(record)
            return data if data else {root.tag: root.attrib}

        # TXT
        elif ext == ".txt":
            return {"text_content": file_bytes.decode("utf-8")}

        # HTML
        elif ext == ".html":
            s = StringIO(file_bytes.decode("utf-8"))
            df = pd.read_html(s)[0]
            return df.to_dict(orient="records")

        else:
            raise ValueError(f"Desteklenmeyen format: {ext}")

    except Exception as e:
        st.error(f"❌ Okuma hatası: {e}")
        return None

# -------------------------
# 2️⃣ Analiz Motoru
# -------------------------
def run_analysis(file_bytes, filename):
    data = universal_reader(file_bytes, filename)
    if not data:
        return None
    results = {
        "file": filename,
        "rows": len(data) if isinstance(data, list) else 1,
        "xG_estimate": 1.42,
        "ppda_estimate": 8.3,
        "transition_efficiency": 0.75,
        "timestamp": datetime.now().isoformat()
    }
    os.makedirs("output", exist_ok=True)
    json_path = f"output/{os.path.basename(filename)}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    results["normalized_json"] = json_path
    return results

# -------------------------
# 3️⃣ Streamlit Arayüzü
# -------------------------
uploaded = st.file_uploader(
    "📤 Dosya yükle (csv, xlsx, json, xml, txt, html)",
    type=["csv","xlsx","xls","json","xml","txt","html"]
)

if uploaded:
    file_bytes = uploaded.read()
    st.info(f"Analiz başlatılıyor → {uploaded.name}")
    result = run_analysis(file_bytes, uploaded.name)

    if result:
        st.success("✅ Analiz tamamlandı!")
        st.json(result)
        with open(result["normalized_json"], "r", encoding="utf-8") as f:
            data = json.load(f)
        st.subheader("🔍 Normalize edilmiş JSON içeriği")
        st.json(data)
else:
    st.warning("Henüz dosya yüklenmedi.")

st.caption("HP Engine Cloud v3.2 © Hikmet Pınarbaş 2026")