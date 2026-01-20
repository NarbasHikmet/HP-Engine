import pandas as pd
import io, pdfplumber
from docx import Document
import xml.etree.ElementTree as ET

class HPReader:
    """Multi-format veri emici: Bilgiyi ampirik veriye dönüştürür."""
    def ingest(self, uploaded_files):
        store = {"data": pd.DataFrame(), "texts": [], "xml_data": []}
        for f in uploaded_files:
            name = f.name.lower()
            content = f.read()
            if name.endswith('.csv'):
                store["data"] = pd.concat([store["data"], pd.read_csv(io.BytesIO(content))], ignore_index=True)
            elif name.endswith('.pdf'):
                with pdfplumber.open(io.BytesIO(content)) as pdf:
                    store["texts"].append(" ".join([p.extract_text() for p in pdf.pages if p.extract_text()]))
            elif name.endswith('.docx'):
                doc = Document(io.BytesIO(content))
                store["texts"].append(" ".join([para.text for para in doc.paragraphs]))
        return store