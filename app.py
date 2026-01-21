import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET
import unicodedata
import re
from io import StringIO

# MUST BE FIRST Streamlit call
st.set_page_config(page_title="HP Engine – CSV/XML Reader", layout="wide")

# Debug banner (optional)
st.write("APP LOADED")

st.title("⚽ HP ENGINE – CSV & XML Reader")
st.caption("Streamlit Cloud uyumlu, UTF-8 / TR destekli")

def normalize_filename(filename: str) -> str:
    name = unicodedata.normalize("NFKD", filename).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", name)

def read_csv_bytes(file_bytes: bytes):
    text = None
    for enc in ("utf-8", "iso-8859-9"):
        try:
            text = file_bytes.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if text is None:
        st.error("Dosya kodlaması okunamadı.")
        return None

    sep = ";" if (";" in text and "," not in text) else (("\t" if "\t" in text else ","))
    try:
        return pd.read_csv(StringIO(text), sep=sep)
    except Exception as e:
        st.error(f"CSV okuma hatası: {e}")
        return None

def read_xml_bytes(file_bytes: bytes):
    try:
        root = ET.fromstring(file_bytes.decode("utf-8", errors="ignore"))
        return {root.tag: {c.tag: c.text for c in root}}
    except Exception as e:
        st.error(f"XML okuma hatası: {e}")
        return None

uploaded = st.file_uploader("CSV veya XML yükle", type=["csv", "xml"])

if uploaded:
    name = normalize_filename(uploaded.name)
    data = uploaded.read()

    if name.lower().endswith(".csv"):
        df = read_csv_bytes(data)
        if df is not None:
            st.success(f"{name} yüklendi (CSV)")
            st.dataframe(df)

    elif name.lower().endswith(".xml"):
        xml = read_xml_bytes(data)
        if xml:
            st.success(f"{name} yüklendi (XML)")
            st.json(xml)