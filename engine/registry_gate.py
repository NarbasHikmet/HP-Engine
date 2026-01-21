from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple, Optional

import pandas as pd


@dataclass
class Eligibility:
    mode: str                 # FULL | DEGRADED | BLOCKED
    reason: str
    missing_fields: Optional[List[str]] = None
    notes: Optional[List[str]] = None


class RegistryGate:
    """
    Contract:
      Input: transformed_df (from SOTValidator), registry yaml
      Output:
        - eligibility_map: metric -> Eligibility
        - coverage_report: summary counts + blocked reasons
    No silent behavior.
    """

    def __init__(self, registry_path: str = "registry/metrics_core_v1.yaml"):
        self.registry_path = registry_path
        self.registry = self._load_yaml(registry_path)
        self.metrics = self.registry.get("metrics", [])

    def evaluate(self, df: pd.DataFrame, strict_constitution: bool = True) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        eligibility_map: Dict[str, Eligibility] = {}

        for m in self.metrics:
            name = m["canonical_name"]

            # Constitution gates
            if strict_constitution:
                # No Unfalsifiable
                if "falsifiability" not in m or not m["falsifiability"]:
                    eligibility_map[name] = Eligibility(
                        mode="BLOCKED",
                        reason="NO_FALSIFIABILITY_BLOCK"
                    )
                    continue

            # Data requirements gates
            req = m.get("data_requirements", {})
            required_fields = req.get("required_fields", [])
            missing = [f for f in required_fields if f not in df.columns]

            if missing:
                # Try DEGRADED if DEGRADED mode exists and missing fields might be optional in proxy
                degraded = m.get("modes", {}).get("DEGRADED")
                if degraded:
                    eligibility_map[name] = Eligibility(
                        mode="DEGRADED",
                        reason="MISSING_FIELDS_USING_PROXY",
                        missing_fields=missing,
                        notes=[degraded.get("proxy_note", "proxy mode")]
                    )
                else:
                    eligibility_map[name] = Eligibility(
                        mode="BLOCKED",
                        reason="MISSING_FIELDS_NO_PROXY",
                        missing_fields=missing
                    )
                continue

            # Additional constitution gate: No Isolated Metrics (graph presence checked later)
            # Here we only mark as FULL/DEGRADED based on requirements; graph gate can be applied in a separate step.
            eligibility_map[name] = Eligibility(mode="FULL", reason="REQUIREMENTS_OK")

        coverage_report = self._coverage_report(eligibility_map)
        # serialize Eligibility objects to dict
        eligibility_serialized = {k: v.__dict__ for k, v in eligibility_map.items()}
        return eligibility_serialized, coverage_report

    def _coverage_report(self, emap: Dict[str, Eligibility]) -> Dict[str, Any]:
        total = len(emap)
        counts = {"FULL": 0, "DEGRADED": 0, "BLOCKED": 0}
        reasons: Dict[str, int] = {}

        for e in emap.values():
            counts[e.mode] = counts.get(e.mode, 0) + 1
            reasons[e.reason] = reasons.get(e.reason, 0) + 1

        return {
            "total_metrics": total,
            "counts": counts,
            "blocked_reasons": dict(sorted(reasons.items(), key=lambda x: -x[1])),
        }

    def _load_yaml(self, path: str) -> Dict[str, Any]:
        try:
            import yaml  # type: ignore
        except Exception as e:
            raise RuntimeError("PyYAML required. Add pyyaml to requirements.txt") from e

        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}