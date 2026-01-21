from __future__ import annotations

from typing import Any, Dict, List, Optional

from .registry_loader import load_registry, get_metric_spec


def list_metric_ids(registry_path: str = "engine/metrics/registry.json", status: Optional[str] = None) -> List[str]:
    reg = load_registry(registry_path).registry
    mids = sorted(list((reg.get("metrics") or {}).keys()))
    if status is None:
        return mids
    out = []
    for mid in mids:
        spec = reg["metrics"][mid]
        if spec.get("status") == status:
            out.append(mid)
    return out


def get_metric(metric_id: str, registry_path: str = "engine/metrics/registry.json") -> Dict[str, Any]:
    reg = load_registry(registry_path).registry
    spec = get_metric_spec(metric_id, reg)
    if spec is None:
        return {
            "found": False,
            "metric_id": metric_id,
            "status": "UNKNOWN",
            "reason": "metric_id not in registry"
        }
    return {
        "found": True,
        "metric_id": metric_id,
        "status": spec.get("status"),
        "spec": spec
    }


def search_metrics(query: str, registry_path: str = "engine/metrics/registry.json") -> List[Dict[str, Any]]:
    """
    Deterministic substring search over:
    - metric_id
    - source.canon_category/subcategory (if present)
    - aliases if later added (not guessed)
    """
    q = (query or "").strip().lower()
    reg = load_registry(registry_path).registry
    results: List[Dict[str, Any]] = []
    for mid, spec in (reg.get("metrics") or {}).items():
        hay = [
            mid.lower(),
            str((spec.get("source") or {}).get("canon_category") or "").lower(),
            str((spec.get("source") or {}).get("canon_subcategory") or "").lower(),
        ]
        if any(q in h for h in hay if h):
            results.append({"metric_id": mid, "status": spec.get("status"), "spec": spec})
    return results