import streamlit as st
import pandas as pd
import json, xml.etree.ElementTree as ET, pdfplumber
from io import StringIO, BytesIO

st.set_page_config(page_title="HP Engine – Universal Reader vFinal", layout="wide")
st.title("⚽ HP ENGINE – Evrensel Dosya Okuyucu (vFinal)")
st.caption("Desteklenen formatlar: CSV, XLSX, JSON, XML, TXT, HTML, PDF")

def read_file(uploaded):
    name = uploaded.name
    ext = name.split(".")[-1].lower()
    content = uploaded.read()

    try:
        if ext == "json":
            return json.loads(content.decode("utf-8"))

        elif ext in ["csv", "tsv"]:
            s = StringIO(content.decode("utf-8"))
            df = pd.read_csv(s)
            return df.to_dict(orient="records")

        elif ext in ["xls", "xlsx"]:
            df = pd.read_excel(BytesIO(content))
            return df.to_dict(orient="records")

        elif ext == "xml":
            xml_str = content.decode("utf-8")
            root = ET.fromstring(xml_str)
            rows = [{c.tag: c.text for c in child} for child in root]
            return rows or {root.tag: root.attrib}

        elif ext == "txt":
            return {"text": content.decode("utf-8")}

        elif ext == "html":
            s = StringIO(content.decode("utf-8"))
            df = pd.read_html(s)[0]
            return df.to_dict(orient="records")

        elif ext == "pdf":
            text_pages = []
            with pdfplumber.open(BytesIO(content)) as pdf:
                for page in pdf.pages:
                    text_pages.append(page.extract_text())
            return {"pdf_text": "\n\n".join(text_pages)}

        else:
            raise ValueError(f"Desteklenmeyen format: {ext}")

    except Exception as e:
        st.error(f"❌ Okuma hatası ({name}): {e}")
        return None

# Streamlit UI
uploaded = st.file_uploader(
    "📤 Dosya yükle (csv, xlsx, json, xml, txt, html, pdf)",
    type=["csv","xlsx","xls","json","xml","txt","html","pdf"]
)

if uploaded:
    st.info(f"İşleniyor → {uploaded.name}")
    data = read_file(uploaded)
    if data:
        st.success("✅ Dosya başarıyla okundu.")
        st.json(data)
    else:
        st.error("Dosya okunamadı.")
else:
    st.warning("Bir dosya yükle (CSV, XLSX, JSON, XML, TXT, HTML, PDF).")