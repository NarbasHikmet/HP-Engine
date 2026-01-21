import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET
import unicodedata
import re
from io import StringIO

st.set_page_config(page_title="HP Engine – CSV/XML Reader", layout="wide")
st.title("⚽ HP ENGINE – CSV & XML Reader")
st.caption("Streamlit Cloud uyumlu, UTF-8 / TR destekli")

def normalize_filename(filename):
    name = unicodedata.normalize("NFKD", filename).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", name)

def read_csv_bytes(file_bytes):
    for enc in ("utf-8", "iso-8859-9"):
        try:
            text = file_bytes.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        st.error("Dosya kodlaması okunamadı.")
        return None

    sep = ";" if ";" in text and "," not in text else ","
    try:
        return pd.read_csv(StringIO(text), sep=sep)
    except Exception as e:
        st.error(str(e))
        return None

def read_xml_bytes(file_bytes):
    try:
        root = ET.fromstring(file_bytes.decode("utf-8", errors="ignore"))
        return {root.tag: {c.tag: c.text for c in root}}
    except Exception as e:
        st.error(str(e))
        return None

uploaded = st.file_uploader("CSV veya XML yükle", type=["csv", "xml"])

if uploaded:
    name = normalize_filename(uploaded.name)
    data = uploaded.read()

    if name.endswith(".csv"):
        df = read_csv_bytes(data)
        if df is not None:
            st.success(f"{name} yüklendi")
            st.dataframe(df)

    elif name.endswith(".xml"):
        xml = read_xml_bytes(data)
        if xml:
            st.success(f"{name} yüklendi")
            st.json(xml)