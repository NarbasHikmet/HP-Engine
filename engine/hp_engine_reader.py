import pandas as pd
import io
import pdfplumber
from docx import Document
import xml.etree.ElementTree as ET

class HPReader:
    def ingest(self, uploaded_files):
        """Multi-format veri emici: CSV, XML, XLSX, PDF, DOCX, TXT."""
        store = {"data": pd.DataFrame(), "texts": [], "xml_data": []}
        
        for f in uploaded_files:
            name = f.name.lower()
            content = f.read()
            
            if name.endswith('.csv'):
                df = pd.read_csv(io.BytesIO(content))
                store["data"] = pd.concat([store["data"], df], ignore_index=True)
            elif name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(io.BytesIO(content))
                store["data"] = pd.concat([store["data"], df], ignore_index=True)
            elif name.endswith('.pdf'):
                with pdfplumber.open(io.BytesIO(content)) as pdf:
                    text = " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])
                    store["texts"].append({"file": name, "content": text})
            elif name.endswith('.docx'):
                doc = Document(io.BytesIO(content))
                text = " ".join([para.text for para in doc.paragraphs])
                store["texts"].append({"file": name, "content": text})
            elif name.endswith('.xml'):
                tree = ET.ElementTree(ET.fromstring(content))
                store["xml_data"].append({"file": name, "content": tree})
            elif name.endswith('.txt'):
                store["texts"].append({"file": name, "content": content.decode("utf-8")})
        
        return store
