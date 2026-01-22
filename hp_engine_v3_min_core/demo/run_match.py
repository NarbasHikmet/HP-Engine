import pandas as pd
import json
from engine.master_orchestrator import MasterOrchestrator

if __name__ == "__main__":
    CSV_PATH = "Maçın Tamamı.csv"  # change if needed
    df = pd.read_csv(CSV_PATH)

    orch = MasterOrchestrator(registry_paths=[
        "canon/registry/tactical/ppda.yaml",
        "canon/registry/tactical/field_tilt.yaml",
    ])

    out = orch.run(df, metrics=["PPDA","FIELD_TILT"])
    print(json.dumps(out, ensure_ascii=False, indent=2))