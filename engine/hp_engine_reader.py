import pandas as pd
import io
import pdfplumber
from docx import Document

class HPReader:
    def ingest(self, uploaded_files):
        store = {"data": pd.DataFrame(), "texts": [], "raw_xml": []}
        for f in uploaded_files:
            name = f.name.lower()
            if name.endswith('.csv'):
                store["data"] = pd.concat([store["data"], pd.read_csv(f)], ignore_index=True)
            elif name.endswith(('.xlsx', '.xls')):
                store["data"] = pd.concat([store["data"], pd.read_excel(f)], ignore_index=True)
            elif name.endswith('.pdf'):
                with pdfplumber.open(f) as pdf:
                    store["texts"].append(" ".join([page.extract_text() for page in pdf.pages]))
            elif name.endswith('.docx'):
                doc = Document(f)
                store["texts"].append(" ".join([para.text for para in doc.paragraphs]))
            elif name.endswith('.txt'):
                store["texts"].append(f.read().decode("utf-8"))
            elif name.endswith('.xml'):
                store["raw_xml"].append(f.read().decode("utf-8"))
        return store
