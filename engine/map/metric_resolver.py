from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


def _norm(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"\s+", " ", s)
    s = s.replace("–", "-").replace("—", "-")
    return s


@dataclass(frozen=True)
class ResolveResult:
    canonical_family: Optional[str]
    match: str
    details: dict


class MetricResolver:
    """
    Canonical resolver using:
      - canon/ontology/metric_ontology.json  (aliases + canonical families)
      - canon/mappings/platform_mappings.json (canonical_to_platforms)

    Note: platform_mappings.json is CANONICAL -> {Platform: MetricName}
          so we invert it at load time to get (platform, raw_metric) -> canonical.
    """

    def __init__(
        self,
        ontology_path: str = "canon/ontology/metric_ontology.json",
        mappings_path: str = "canon/mappings/platform_mappings.json",
    ) -> None:
        self.ontology_path = Path(ontology_path)
        self.mappings_path = Path(mappings_path)

        self.ontology = self._load_json(self.ontology_path)
        self.mappings = self._load_json(self.mappings_path)

        # Build alias index from ontology
        self.alias_to_canonical: dict[str, str] = {}
        fams = (self.ontology or {}).get("canonical_families", {})
        if isinstance(fams, dict):
            for canonical, meta in fams.items():
                self.alias_to_canonical[_norm(canonical)] = canonical
                if isinstance(meta, dict):
                    nm = meta.get("name")
                    if isinstance(nm, str) and nm.strip():
                        self.alias_to_canonical[_norm(nm)] = canonical
                    for a in (meta.get("aliases", []) or []):
                        self.alias_to_canonical[_norm(a)] = canonical
                    short = meta.get("short")
                    if isinstance(short, str) and short.strip():
                        self.alias_to_canonical[_norm(short)] = canonical

        # Invert canonical_to_platforms to (platform, raw_metric) -> canonical
        self.platform_raw_to_canonical: dict[tuple[str, str], str] = {}
        c2p = (self.mappings or {}).get("canonical_to_platforms", {})
        if isinstance(c2p, dict):
            for canonical_short, plat_map in c2p.items():
                if not isinstance(plat_map, dict):
                    continue
                # Map short key (e.g., "xG") to canonical family via ontology if possible
                canonical_family = self.alias_to_canonical.get(_norm(canonical_short), canonical_short)
                for platform, raw_name in plat_map.items():
                    if isinstance(platform, str) and isinstance(raw_name, str):
                        self.platform_raw_to_canonical[(_norm(platform), _norm(raw_name))] = canonical_family

    @staticmethod
    def _load_json(p: Path) -> Any:
        if not p.exists():
            raise FileNotFoundError(f"Missing file: {p.as_posix()}")
        return json.loads(p.read_text(encoding="utf-8"))

    def resolve(self, raw_metric_name: str, platform: Optional[str] = None) -> ResolveResult:
        raw_n = _norm(raw_metric_name)
        plat_n = _norm(platform) if platform else None
        details: dict = {"raw": raw_metric_name, "raw_norm": raw_n, "platform": platform}

        # 1) platform mapping (strongest)
        if plat_n:
            hit = self.platform_raw_to_canonical.get((plat_n, raw_n))
            if hit:
                return ResolveResult(canonical_family=hit, match="platform_mapping_inverted", details=details)

        # 2) ontology alias/name/short
        hit = self.alias_to_canonical.get(raw_n)
        if hit:
            return ResolveResult(canonical_family=hit, match="ontology_alias", details=details)

        return ResolveResult(canonical_family=None, match="unknown", details=details)