from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple
import pandas as pd

@dataclass
class ValidationReport:
    status: str  # HEALTHY / DEGRADED / BLOCKED
    issues: List[str]
    null_map: Dict[str, int]
    notes: List[str]

class SOTValidator:
    """Contract gate: validates and reports; does not silently drop rows."""
    def __init__(self, required_cols: List[str]):
        self.required_cols = required_cols

    def validate(self, df: pd.DataFrame) -> Tuple[ValidationReport, pd.DataFrame]:
        issues: List[str] = []
        notes: List[str] = []
        status = "HEALTHY"

        missing = [c for c in self.required_cols if c not in df.columns]
        if missing:
            status = "BLOCKED"
            issues.append(f"MISSING_REQUIRED_COLUMNS:{missing}")

        if "timestamp_s" in df.columns:
            if df["timestamp_s"].isna().mean() > 0.05:
                status = "DEGRADED" if status != "BLOCKED" else status
                issues.append("TIMESTAMP_NA_RATE_GT_5PCT")
            if df["timestamp_s"].dropna().max() > 200*60:
                notes.append("Timestamp exceeds 200 minutes; ensure units are seconds.")

        if "x" in df.columns and "y" in df.columns:
            out = (~df["x"].between(0,105)) | (~df["y"].between(0,68))
            out_rate = float(out.mean()) if len(df) else 0.0
            if out_rate > 0.02:
                status = "DEGRADED" if status != "BLOCKED" else status
                issues.append(f"COORD_OUT_OF_RANGE_RATE:{out_rate:.3f}")
                notes.append("Out-of-range coords are kept (no drop). Downstream metrics may be degraded.")

        null_map = df.isnull().sum().to_dict()
        return ValidationReport(status=status, issues=issues, null_map=null_map, notes=notes), df