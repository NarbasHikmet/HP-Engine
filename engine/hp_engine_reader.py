# engine/hp_engine_reader.py
import pandas as pd
import json, xml.etree.ElementTree as ET, docx, os

def universal_reader(file_path):
    ext = os.path.splitext(file_path)[-1].lower()

    # JSON
    if ext == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # CSV
    elif ext in [".csv", ".tsv"]:
        df = pd.read_csv(file_path)
        return df.to_dict(orient="records")

    # Excel
    elif ext in [".xls", ".xlsx"]:
        df = pd.read_excel(file_path)
        return df.to_dict(orient="records")

    # XML
    elif ext == ".xml":
        tree = ET.parse(file_path)
        root = tree.getroot()
        return {root.tag: {child.tag: child.text for child in root}}

    # TXT
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return {"text_content": f.read()}

    # HTML
    elif ext == ".html":
        df = pd.read_html(file_path)[0]
        return df.to_dict(orient="records")

    # DOCX
    elif ext == ".docx":
        doc = docx.Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
        return {"doc_content": text}

    else:
        raise ValueError(f"Unsupported file format: {ext}")

def normalize_to_json(data, save_path):
    """Veriyi JSON formatına dönüştürür ve kaydeder."""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return save_path