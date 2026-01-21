from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple, Optional

import pandas as pd


@dataclass
class ValidationIssue:
    code: str
    severity: str  # INFO | WARN | ERROR
    message: str
    details: Optional[Dict[str, Any]] = None


class SOTValidator:
    """
    Contract-first validator.
    - NO silent drop.
    - 0.0 is valid.
    - Produces (report, transformed_df).
    """

    def __init__(self, contract_path: str = "canon/provider_contracts/SportsBase.yaml"):
        self.contract_path = contract_path
        self.contract = self._load_yaml(contract_path)
        self.canonical_dim = (105.0, 68.0)

    def validate(self, raw_df: pd.DataFrame) -> Tuple[Dict[str, Any], pd.DataFrame]:
        issues: List[ValidationIssue] = []
        status = "HEALTHY"

        # 1) Required columns
        required_cols = self.contract.get("required_columns", [])
        missing = [c for c in required_cols if c not in raw_df.columns]
        if missing:
            issues.append(ValidationIssue(
                code="MISSING_COLUMNS",
                severity="ERROR",
                message="Required columns missing",
                details={"missing": missing}
            ))
            status = "BLOCKED"

        # If blocked, still return report with original df (no drop)
        if status == "BLOCKED":
            return self._build_report(status, issues, raw_df), raw_df

        df = raw_df.copy()

        # 2) Basic type sanity (soft; do not coerce destructively)
        for col in ["x", "y", "timestamp"]:
            if col in df.columns:
                # Try to coerce to numeric without dropping; non-numeric becomes NaN -> reported
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # 3) Coordinate transform provider -> canonical (NO drop)
        df = self._transform_coordinates(df, issues)

        # 4) Range checks (flag, not drop)
        df = self._flag_out_of_bounds(df, issues)

        # 5) Timebase checks (per match monotonic non-decreasing)
        if not self._check_timebase(df, issues):
            status = "DEGRADED" if status != "BLOCKED" else status

        # 6) Null map (explicit)
        null_map = df.isnull().sum().to_dict()
        # If critical nulls exist, degrade (not drop)
        critical_nulls = {k: v for k, v in null_map.items() if k in ["x_m", "y_m", "timestamp"] and v > 0}
        if critical_nulls:
            issues.append(ValidationIssue(
                code="CRITICAL_NULLS",
                severity="WARN",
                message="Critical nulls found after coercion/transform; metrics may be DEGRADED/BLOCKED by RegistryGate.",
                details={"critical_nulls": critical_nulls}
            ))
            status = "DEGRADED"

        report = self._build_report(status, issues, df, extra={"null_map": null_map})
        return report, df

    # ----------------- helpers -----------------

    def _transform_coordinates(self, df: pd.DataFrame, issues: List[ValidationIssue]) -> pd.DataFrame:
        coord = self.contract.get("coordinate_system", {})
        provider_scale = coord.get("provider_scale", "0_100")

        # Expect provider x,y in 0..100 if provider_scale says so.
        # Transform to meters x_m, y_m. Keep original x,y.
        if "x" not in df.columns or "y" not in df.columns:
            issues.append(ValidationIssue(
                code="COORD_MISSING",
                severity="ERROR",
                message="x/y columns missing for coordinate transform"
            ))
            return df

        if provider_scale == "0_100":
            df["x_m"] = (df["x"] / 100.0) * self.canonical_dim[0]
            df["y_m"] = (df["y"] / 100.0) * self.canonical_dim[1]
        else:
            # If already in meters or unknown, pass-through with explicit flag
            df["x_m"] = df["x"]
            df["y_m"] = df["y"]
            issues.append(ValidationIssue(
                code="COORD_SCALE_UNKNOWN",
                severity="WARN",
                message="Provider coordinate scale not recognized; using pass-through for x_m/y_m",
                details={"provider_scale": provider_scale}
            ))
        return df

    def _flag_out_of_bounds(self, df: pd.DataFrame, issues: List[ValidationIssue]) -> pd.DataFrame:
        # Flag provider bounds and canonical bounds separately; do not drop.
        prov_ranges = self.contract.get("ranges", {})
        px0, px1 = prov_ranges.get("provider_x", [0.0, 100.0])
        py0, py1 = prov_ranges.get("provider_y", [0.0, 100.0])
        cx0, cx1 = prov_ranges.get("canonical_x", [0.0, 105.0])
        cy0, cy1 = prov_ranges.get("canonical_y", [0.0, 68.0])

        df["oob_provider"] = False
        df.loc[(df["x"] < px0) | (df["x"] > px1) | (df["y"] < py0) | (df["y"] > py1), "oob_provider"] = True

        df["oob_canonical"] = False
        df.loc[(df["x_m"] < cx0) | (df["x_m"] > cx1) | (df["y_m"] < cy0) | (df["y_m"] > cy1), "oob_canonical"] = True

        oob_count = int(df["oob_canonical"].sum())
        if oob_count > 0:
            issues.append(ValidationIssue(
                code="OUT_OF_BOUNDS",
                severity="WARN",
                message="Out-of-bounds coordinates detected; flagged (no drop).",
                details={"oob_canonical_count": oob_count}
            ))
        return df

    def _check_timebase(self, df: pd.DataFrame, issues: List[ValidationIssue]) -> bool:
        match_key = self.contract.get("identity", {}).get("match_key", "match_id")
        time_field = self.contract.get("timebase", {}).get("field", "timestamp")
        allow_equal = bool(self.contract.get("timebase", {}).get("allow_equal", True))

        if match_key not in df.columns or time_field not in df.columns:
            issues.append(ValidationIssue(
                code="TIMEBASE_FIELDS_MISSING",
                severity="ERROR",
                message="Timebase fields missing; cannot validate sequence ordering.",
                details={"match_key": match_key, "time_field": time_field}
            ))
            return False

        ok = True
        for match_id, g in df.groupby(match_key, dropna=False):
            ts = g[time_field]
            # If NaNs exist, degrade but continue
            if ts.isnull().any():
                issues.append(ValidationIssue(
                    code="TIMEBASE_NULLS",
                    severity="WARN",
                    message="Null timestamps detected; temporal metrics likely DEGRADED.",
                    details={"match_id": str(match_id), "null_count": int(ts.isnull().sum())}
                ))
                ok = False
                continue

            diffs = ts.diff()
            if allow_equal:
                bad = (diffs < 0).any()
            else:
                bad = (diffs <= 0).any()

            if bool(bad):
                issues.append(ValidationIssue(
                    code="TEMPORAL_INCONSISTENCY",
                    severity="WARN",
                    message="Non-monotonic timestamp ordering detected within match; flagged.",
                    details={"match_id": str(match_id)}
                ))
                ok = False
        return ok

    def _build_report(self, status: str, issues: List[ValidationIssue], df: pd.DataFrame, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        out = {
            "status": status,
            "issues": [issue.__dict__ for issue in issues],
            "row_count": int(len(df)),
            "columns": list(df.columns),
        }
        if extra:
            out.update(extra)
        return out

    def _load_yaml(self, path: str) -> Dict[str, Any]:
        # Minimal YAML loader without extra dependencies:
        # If you already use PyYAML in repo, replace with yaml.safe_load for reliability.
        try:
            import yaml  # type: ignore
        except Exception as e:
            raise RuntimeError("PyYAML required. Add pyyaml to requirements.txt") from e

        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}