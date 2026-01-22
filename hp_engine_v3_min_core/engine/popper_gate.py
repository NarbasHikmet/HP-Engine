from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Claim:
    metric: str
    status: str  # VERIFIED / DEGRADED / BLOCKED
    confidence: float
    rationale: Dict[str, Any]

class PopperGate:
    """Minimal v1 Popper gate: no strong claim from BLOCKED metrics; DEGRADED yields weaker claims."""
    def verify(self, metric_results) -> List[Claim]:
        claims: List[Claim] = []
        for r in metric_results:
            if r.status == "BLOCKED":
                claims.append(Claim(metric=r.name, status="BLOCKED", confidence=0.0, rationale={"reason": r.details.get("reason","BLOCKED")}))
                continue
            conf = 0.75 if r.status == "FULL" else 0.60
            # simple sample-size penalty for PPDA / FieldTilt
            if isinstance(r.value, dict) and "match" in r.value and r.value["match"]:
                any_team = next(iter(r.value["match"].keys()))
                counts = r.value["match"][any_team]
                for k in ("opp_passes_in_zone","def_actions_in_zone","total_final_third_passes"):
                    if k in counts and counts[k] is not None and counts[k] < 30:
                        conf -= 0.10
            conf = max(0.0, min(1.0, conf))
            claims.append(Claim(metric=r.name, status=("VERIFIED" if r.status=="FULL" else "DEGRADED"), confidence=conf, rationale={"metric_status": r.status}))
        return claims