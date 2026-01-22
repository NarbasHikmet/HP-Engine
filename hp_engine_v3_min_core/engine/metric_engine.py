from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, List
import yaml
import pandas as pd

from .metrics.ppda import calc_ppda_v1
from .metrics.field_tilt import calc_field_tilt_v1

LOGIC_METHODS = {
    "calc_ppda_v1": calc_ppda_v1,
    "calc_field_tilt_v1": calc_field_tilt_v1,
}

@dataclass
class MetricResult:
    name: str
    status: str  # FULL/DEGRADED/BLOCKED
    value: Any
    details: Dict[str, Any]

class MetricEngine:
    def __init__(self, registry_paths: List[str]):
        self.registry: Dict[str, Dict[str, Any]] = {}
        for p in registry_paths:
            with open(p, "r", encoding="utf-8") as f:
                m = yaml.safe_load(f)
            self.registry[m["canonical_name"]] = m

    def compute(self, df: pd.DataFrame, metrics: List[str]) -> List[MetricResult]:
        results: List[MetricResult] = []
        for name in metrics:
            if name not in self.registry:
                results.append(MetricResult(name=name, status="BLOCKED", value=None, details={"reason":"NOT_IN_REGISTRY"}))
                continue
            spec = self.registry[name]
            fn = LOGIC_METHODS.get(spec.get("logic_method"))
            if fn is None:
                results.append(MetricResult(name=name, status="BLOCKED", value=None, details={"reason":"UNKNOWN_LOGIC_METHOD", "logic_method": spec.get("logic_method")}))
                continue
            missing = [c for c in spec["data_requirements"]["required_columns_canonical"] if c not in df.columns]
            if missing:
                results.append(MetricResult(name=name, status="BLOCKED", value=None, details={"reason":"MISSING_REQUIRED_COLUMNS", "missing": missing}))
                continue
            val, meta = fn(df, spec)
            results.append(MetricResult(name=name, status=meta.get("status","FULL"), value=val, details=meta))
        return results