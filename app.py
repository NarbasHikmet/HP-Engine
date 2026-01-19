import streamlit as st
import pandas as pd
import json, xml.etree.ElementTree as ET
from io import StringIO, BytesIO

st.set_page_config(page_title="HP Engine – File Reader", layout="wide")
st.title("⚽ HP ENGINE – Hızlı Dosya Okuma")
st.caption("CSV · XLSX · JSON · XML")

def read_file(file_bytes, name):
    ext = name.split(".")[-1].lower()

    if ext == "json":
        return json.loads(file_bytes.decode("utf-8"))

    if ext in ["csv", "tsv"]:
        return pd.read_csv(StringIO(file_bytes.decode("utf-8"))).to_dict(orient="records")

    if ext in ["xls", "xlsx"]:
        return pd.read_excel(BytesIO(file_bytes)).to_dict(orient="records")

    if ext == "xml":
        root = ET.fromstring(file_bytes.decode("utf-8"))
        rows = [{c.tag: c.text for c in child} for child in root]
        return rows or {root.tag: root.attrib}

    raise ValueError(f"Desteklenmeyen format: {ext}")

file = st.file_uploader("📂 Dosya yükle", type=["csv","xlsx","xls","json","xml"])
if file:
    try:
        data = read_file(file.read(), file.name)
        st.success("✅ Dosya başarıyla okundu.")
        st.json(data)
    except Exception as e:
        st.error(f"❌ Okuma hatası: {e}")
else:
    st.info("Bir dosya seç ve yükle.")