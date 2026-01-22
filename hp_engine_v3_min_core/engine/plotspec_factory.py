from __future__ import annotations
from typing import List, Dict, Any

class PlotSpecFactory:
    def generate(self, metric_results) -> List[Dict[str, Any]]:
        specs: List[Dict[str, Any]] = []
        for r in metric_results:
            if r.status == "BLOCKED":
                continue
            if r.name == "PPDA":
                specs.append({
                    "type": "line_by_timebin",
                    "metric": "PPDA",
                    "y": "ppda",
                    "notes": r.details.get("zone_definition"),
                })
            if r.name == "FIELD_TILT":
                specs.append({
                    "type": "line_by_timebin",
                    "metric": "FIELD_TILT",
                    "y": "field_tilt",
                    "notes": r.details.get("final_third_definition"),
                })
        return specs