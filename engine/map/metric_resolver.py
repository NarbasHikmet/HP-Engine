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
    canonical: Optional[str]
    match: str
    details: dict


class MetricResolver:
    """
    Platform + alias aware canonical resolver.

    Files (repo-relative):
      - canon/ontology/metric_ontology.json
      - canon/mappings/platform_mappings.json
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

        self.alias_to_canonical: dict[str, str] = {}
        for canonical, meta in (self.ontology or {}).items():
            if isinstance(meta, dict):
                for a in (meta.get("aliases", []) or []):
                    self.alias_to_canonical[_norm(a)] = canonical
                nm = meta.get("name")
                if isinstance(nm, str) and nm.strip():
                    self.alias_to_canonical[_norm(nm)] = canonical
            self.alias_to_canonical[_norm(canonical)] = canonical

    @staticmethod
    def _load_json(p: Path) -> Any:
        if not p.exists():
            raise FileNotFoundError(f"Missing file: {p.as_posix()}")
        return json.loads(p.read_text(encoding="utf-8"))

    def resolve(self, raw_metric_name: str, platform: Optional[str] = None) -> ResolveResult:
        raw_n = _norm(raw_metric_name)
        plat_n = _norm(platform) if platform else None
        details: dict = {"raw": raw_metric_name, "raw_norm": raw_n, "platform": platform}

        # 1) platform mapping
        if plat_n:
            plat_map = self.mappings.get(plat_n)
            if isinstance(plat_map, dict):
                hit = plat_map.get(raw_metric_name)
                if hit is None:
                    hit = plat_map.get(raw_n)

                if isinstance(hit, str):
                    return ResolveResult(canonical=hit, match="platform_mapping:string", details=details)

                if isinstance(hit, dict):
                    canonical = hit.get("canonical") or hit.get("canonical_family")
                    return ResolveResult(canonical=canonical, match="platform_mapping:dict", details={**details, **hit})

        # 2) ontology alias/name
        canonical = self.alias_to_canonical.get(raw_n)
        if canonical:
            return ResolveResult(canonical=canonical, match="ontology_alias", details=details)

        return ResolveResult(canonical=None, match="unknown", details=details)