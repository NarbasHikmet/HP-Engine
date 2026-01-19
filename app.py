import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET
import json, chardet
from io import StringIO, BytesIO

st.set_page_config(page_title="HP Engine – CSV & XML Reader", layout="wide")
st.title("⚽ HP ENGINE – CSV & XML Reader vFinal")
st.caption("Galatasaray & UEFA veri dosyaları için optimize edilmiştir")

# -------------------------------
# 1️⃣ Karakter kodlamasını tespit et
# -------------------------------
def detect_encoding(file_bytes):
    detection = chardet.detect(file_bytes)
    return detection.get("encoding", "utf-8")

# -------------------------------
# 2️⃣ CSV Okuyucu
# -------------------------------
def read_csv(file_bytes):
    enc = detect_encoding(file_bytes)
    text = file_bytes.decode(enc, errors="replace")

    # Otomatik ayraç tespiti
    if ";" in text and "," not in text:
        sep = ";"
    elif "\t" in text:
        sep = "\t"
    else:
        sep = ","

    df = pd.read_csv(StringIO(text), sep=sep)
    return df.to_dict(orient="records")

# -------------------------------
# 3️⃣ XML Okuyucu
# -------------------------------
def read_xml(file_bytes):
    enc = detect_encoding(file_bytes)
    xml_str = file_bytes.decode(enc, errors="replace")
    root = ET.fromstring(xml_str)

    def parse_element(element):
        parsed = {element.tag: {} if element.attrib else None}
        children = list(element)
        if children:
            dd = {}
            for dc in map(parse_element, children):
                for k, v in dc.items():
                    if k in dd:
                        if isinstance(dd[k], list):
                            dd[k].append(v)
                        else:
                            dd[k] = [dd[k], v]
                    else:
                        dd[k] = v
            parsed[element.tag] = dd
        if element.attrib:
            parsed[element.tag].update(('@' + k, v) for k, v in element.attrib.items())
        if element.text and element.text.strip():
            text = element.text.strip()
            if children or element.attrib:
                parsed[element.tag]['#text'] = text
            else:
                parsed[element.tag] = text
        return parsed

    return parse_element(root)

# -------------------------------
# 4️⃣ Arayüz
# -------------------------------
uploaded = st.file_uploader("📤 Dosya yükle (CSV veya XML)", type=["csv", "xml"])
if uploaded:
    bytes_data = uploaded.read()
    ext = uploaded.name.split(".")[-1].lower()

    try:
        if ext == "csv":
            data = read_csv(bytes_data)
        elif ext == "xml":
            data = read_xml(bytes_data)
        else:
            st.error("Desteklenmeyen format.")
            data = None

        if data:
            st.success("✅ Dosya başarıyla okundu.")
            st.json(data)
    except Exception as e:
        st.error(f"❌ Okuma hatası: {e}")
else:
    st.info("Galatasaray veya UEFA dosyasını (.csv veya .xml) yükle.")

st.caption("HP Engine CSV+XML Core v4.0 © Hikmet Pınarbaş 2026")