from __future__ import annotations
from typing import Dict, Any

class AureliaNarrative:
    def produce(self, claims, metric_results) -> Dict[str, Any]:
        out = {"headline": [], "limitations": [], "claims": []}
        res_map = {r.name: r for r in metric_results}

        for c in claims:
            out["claims"].append({
                "metric": c.metric,
                "status": c.status,
                "confidence": round(c.confidence, 2),
                "rationale": c.rationale
            })

        if "PPDA" in res_map and res_map["PPDA"].status != "BLOCKED":
            out["headline"].append("Pressing profile computed (PPDA).")
            if res_map["PPDA"].status != "FULL":
                out["limitations"].append("PPDA DEGRADED: defensive action taxonomy coverage is low in provider export.")
        if "FIELD_TILT" in res_map and res_map["FIELD_TILT"].status != "BLOCKED":
            out["headline"].append("Territorial control computed (Field Tilt).")

        if not out["headline"]:
            out["headline"].append("No publishable outputs (all metrics BLOCKED).")

        return out