import pandas as pd
import io, pdfplumber
from docx import Document

class HPReader:
    def ingest(self, uploaded_files):
        store = {"data": pd.DataFrame(), "texts": [], "xml_data": []}
        for f in uploaded_files:
            name = f.name.lower()
            buffer = io.BytesIO(f.read())
            
            if name.endswith('.csv'):
                store["data"] = pd.concat([store["data"], pd.read_csv(buffer)], ignore_index=True)
            elif name.endswith('.pdf'):
                with pdfplumber.open(buffer) as pdf:
                    text = " ".join([p.extract_text() for p in pdf.pages if p.extract_text()])
                    store["texts"].append(text)
            elif name.endswith('.docx'):
                doc = Document(buffer)
                text = " ".join([p.text for p in doc.paragraphs])
                store["texts"].append(text)
        return store
