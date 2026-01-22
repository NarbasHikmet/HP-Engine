from __future__ import annotations
from typing import Dict, Any, List
import pandas as pd

from .provider.sportsbase import to_canonical_events
from .sot_validator import SOTValidator
from .metric_engine import MetricEngine
from .popper_gate import PopperGate
from .plotspec_factory import PlotSpecFactory
from .aurelia_narrative import AureliaNarrative

class MasterOrchestrator:
    """Pipeline: Ingestion -> SOT -> Metrics -> Popper -> PlotSpec -> Narrative."""
    def __init__(self, registry_paths: List[str]):
        self.metric_engine = MetricEngine(registry_paths=registry_paths)
        self.popper = PopperGate()
        self.plotspec = PlotSpecFactory()
        self.aurelia = AureliaNarrative()

    def run(self, raw_df: pd.DataFrame, metrics: List[str]) -> Dict[str, Any]:
        mapped = to_canonical_events(raw_df)
        canonical_df = mapped.canonical_df

        validator = SOTValidator(required_cols=["match_id","team_id","event_type","timestamp_s","x","y"])
        val_report, canon_df = validator.validate(canonical_df)

        metric_results = self.metric_engine.compute(canon_df, metrics=metrics)
        claims = self.popper.verify(metric_results)
        specs = self.plotspec.generate(metric_results)
        narrative = self.aurelia.produce(claims, metric_results)

        return {
            "provider_mapping": mapped.mapping_used,
            "validation_report": {
                "status": val_report.status,
                "issues": val_report.issues,
                "notes": val_report.notes,
                "null_map": val_report.null_map
            },
            "metrics": {r.name: {"status": r.status, "value": r.value, "details": r.details} for r in metric_results},
            "claims": [c.__dict__ for c in claims],
            "plotspecs": specs,
            "narrative": narrative
        }