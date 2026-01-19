import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET
import unicodedata
import re
from io import StringIO, BytesIO

st.set_page_config(page_title="HP Engine – CSV/XML Reader", layout="wide")
st.title("⚽ HP ENGINE – Mobil Uyumlu CSV & XML Okuyucu (Final)")
st.caption("Sadece CSV ve XML dosyaları. Türkçe karakter desteği, mobil uyumlu bellek içi okuma.")

# 🔤 1️⃣ Dosya adı temizleyici
def normalize_filename(filename):
    name = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
    name = re.sub(r'[^a-zA-Z0-9_.-]', '_', name)
    return name

# 📊 2️⃣ CSV okuyucu
def read_csv_bytes(file_bytes):
    text = None
    try:
        text = file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        try:
            text = file_bytes.decode("iso-8859-9")
        except:
            st.error("⚠️ Dosya kodlaması okunamadı (UTF-8 veya ISO-8859-9 değil).")
            return None

    if ";" in text and "," not in text:
        sep = ";"
    elif "\t" in text:
        sep = "\t"
    else:
        sep = ","

    try:
        df = pd.read_csv(StringIO(text), sep=sep)
        return df
    except Exception as e:
        st.error(f"❌ CSV okuma hatası: {e}")
        return None

# 🧩 3️⃣ XML okuyucu
def read_xml_bytes(file_bytes):
    try:
        xml_text = file_bytes.decode("utf-8", errors="ignore")
        root = ET.fromstring(xml_text)

        def parse_element(elem):
            children = list(elem)
            if len(children) > 0:
                return {elem.tag: {c.tag: parse_element(c) for c in children}}
            else:
                return elem.text

        parsed = {root.tag: parse_element(root)}
        return parsed
    except Exception as e:
        st.error(f"❌ XML okuma hatası: {e}")
        return None

# 🎛️ 4️⃣ Streamlit Arayüzü
uploaded = st.file_uploader("📂 CSV veya XML dosyasını yükle", type=["csv", "xml"])

if uploaded:
    filename = normalize_filename(uploaded.name)
    file_bytes = uploaded.read()

    if len(file_bytes) == 0:
        st.error("⚠️ Dosya yüklenemedi. Lütfen tekrar seç.")
    else:
        ext = filename.split(".")[-1].lower()

        if ext == "csv":
            df = read_csv_bytes(file_bytes)
            if df is not None:
                st.success(f"✅ {filename} başarıyla okundu (CSV)")
                st.dataframe(df)
        elif ext == "xml":
            data = read_xml_bytes(file_bytes)
            if data:
                st.success(f"✅ {filename} başarıyla okundu (XML)")
                st.json(data)
        else:
            st.error("❌ Sadece CSV veya XML yükleyebilirsin.")
else:
    st.info("Telefonundan CSV veya XML dosyası seç ve yükle.")

st.caption("HP Engine Cloud v5.0 – © Hikmet Pınarbaş 2026")