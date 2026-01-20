import pandas as pd
import io

class Reader:
    def ingest(self, uploaded_files):
        store = {"events": pd.DataFrame(), "metrics": pd.DataFrame()}
        for f in uploaded_files:
            name = f.name.lower()
            try:
                df = pd.read_csv(f) if name.endswith('.csv') else pd.read_excel(f)
                # 'action' kolonu varsa event, yoksa metric kabul et
                if "action" in [str(c).lower() for c in df.columns]:
                    store["events"] = pd.concat([store["events"], df], ignore_index=True)
                else:
                    store["metrics"] = pd.concat([store["metrics"], df], ignore_index=True)
            except Exception as e:
                print(f"Hata: {name} okunamadı: {e}")
        return store
