from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# --- Canon/registry locations (repo-relative) ---
CANDIDATE_REGISTRY_PATHS: Tuple[str, ...] = (
    "canon/metrics/registry.json",
    "canon/metrics/registry/registry.json",
    "canon/metrics/registry/index.json",
)

CANDIDATE_SPEC_ROOTS: Tuple[str, ...] = (
    "canon/metrics/specs",
    "canon/metrics",  # fallback: some repos put specs directly here
)

SPEC_SUFFIXES: Tuple[str, ...] = (
    ".metric_spec.json",
    ".metricspec.json",
    ".spec.json",
)


@dataclass(frozen=True)
class MetricDoc:
    metric_id: str
    doc: Dict[str, Any]
    source_path: str


def _repo_root() -> Path:
    # engine/metrics/api.py -> engine/metrics -> engine -> repo root
    return Path(__file__).resolve().parents[2]


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _find_registry_file(root: Path) -> Optional[Path]:
    for rel in CANDIDATE_REGISTRY_PATHS:
        p = root / rel
        if p.exists() and p.is_file():
            return p
    return None


def _iter_spec_files(root: Path) -> List[Path]:
    files: List[Path] = []
    for spec_root_rel in CANDIDATE_SPEC_ROOTS:
        base = root / spec_root_rel
        if not base.exists():
            continue
        if base.is_file():
            continue
        for suf in SPEC_SUFFIXES:
            files.extend(base.rglob(f"*{suf}"))
    # unique + stable order
    uniq = sorted({p.resolve() for p in files})
    return uniq


def _load_registry_ids(registry_path: Path) -> List[str]:
    """
    Registry formats tolerated:
      - {"metrics": [{"metric_id": "..."} , ...]}
      - {"metric_ids": ["...", "..."]}
      - ["...", "..."]
    """
    reg = _read_json(registry_path)

    if isinstance(reg, list):
        return [str(x) for x in reg]

    if isinstance(reg, dict):
        if isinstance(reg.get("metric_ids"), list):
            return [str(x) for x in reg["metric_ids"]]
        if isinstance(reg.get("metrics"), list):
            out: List[str] = []
            for m in reg["metrics"]:
                if isinstance(m, dict) and "metric_id" in m:
                    out.append(str(m["metric_id"]))
            return out

    # unknown format -> empty (caller will fallback to scan)
    return []


def _scan_specs_for_ids(spec_files: List[Path]) -> Tuple[List[str], List[Dict[str, str]]]:
    """
    Returns:
      - metric_ids
      - errors (list of {"path":..., "error":...})
    Never raises on bad JSON; collects errors instead.
    """
    metric_ids: List[str] = []
    errors: List[Dict[str, str]] = []

    for p in spec_files:
        try:
            doc = _read_json(p)
            if isinstance(doc, dict) and "metric_id" in doc:
                metric_ids.append(str(doc["metric_id"]))
            else:
                errors.append({"path": p.as_posix(), "error": "missing metric_id"})
        except Exception as e:
            errors.append({"path": p.as_posix(), "error": f"{type(e).__name__}: {e}"})

    # de-dupe stable
    seen = set()
    uniq: List[str] = []
    for mid in metric_ids:
        if mid not in seen:
            uniq.append(mid)
            seen.add(mid)

    return uniq, errors


def list_metric_ids(debug: bool = False) -> List[str]:
    """
    Primary entry used by CI.
    Behavior:
      1) If a registry file exists and yields >=1 ids, return those ids.
      2) Else scan canon metric spec files and return discovered ids.
    If debug=True, prints diagnostics to stdout (useful in CI logs).
    """
    root = _repo_root()

    reg_path = _find_registry_file(root)
    if reg_path:
        try:
            ids = _load_registry_ids(reg_path)
            if ids:
                if debug:
                    print({"source": "registry", "path": reg_path.as_posix(), "count": len(ids), "sample": ids[:10]})
                return ids
            if debug:
                print({"source": "registry", "path": reg_path.as_posix(), "warning": "registry empty/unknown format"})
        except Exception as e:
            if debug:
                print({"source": "registry", "path": reg_path.as_posix(), "error": f"{type(e).__name__}: {e}"})

    spec_files = _iter_spec_files(root)
    ids, errors = _scan_specs_for_ids(spec_files)

    if debug:
        print({"source": "scan", "spec_files": len(spec_files), "count": len(ids), "sample": ids[:10]})
        if errors:
            # only print a few to keep logs readable
            print({"scan_errors": errors[:10], "scan_errors_total": len(errors)})

    return ids


def get_metric(metric_id: str) -> Optional[MetricDoc]:
    """
    Best-effort metric loader.
    - If registry exists and has pointers, we ignore pointers (since format unknown).
    - We scan spec files and return the first match.
    """
    root = _repo_root()
    metric_id = str(metric_id)

    spec_files = _iter_spec_files(root)
    for p in spec_files:
        try:
            doc = _read_json(p)
            if isinstance(doc, dict) and str(doc.get("metric_id")) == metric_id:
                return MetricDoc(metric_id=metric_id, doc=doc, source_path=p.as_posix())
        except Exception:
            continue
    return None


def search_metrics(query: str, limit: int = 20) -> List[MetricDoc]:
    """
    Very simple search across metric_id/full_name/short_name/aliases (best-effort).
    """
    q = (query or "").strip().lower()
    if not q:
        return []

    root = _repo_root()
    out: List[MetricDoc] = []
    for p in _iter_spec_files(root):
        try:
            doc = _read_json(p)
            if not isinstance(doc, dict):
                continue
            mid = str(doc.get("metric_id", ""))
            blob = " ".join(
                [
                    mid,
                    str(doc.get("full_name", "")),
                    str(doc.get("short_name", "")),
                    " ".join([str(x) for x in (doc.get("aliases") or []) if isinstance(x, (str, int, float))]),
                ]
            ).lower()
            if q in blob:
                out.append(MetricDoc(metric_id=mid, doc=doc, source_path=p.as_posix()))
                if len(out) >= int(limit):
                    break
        except Exception:
            continue
    return out