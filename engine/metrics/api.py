from __future__ import annotations

from typing import Any, Dict, List, Optional

from .football_metrics_encyclopedia import (
    METRICS,
    MetricCategory,
    MetricDefinition,
    get_metric as _get_metric,
    get_summary as _get_summary,
    search_metrics as _search_metrics,
) 

__all__ = [
    "METRICS",
    "MetricCategory",
    "MetricDefinition",
    "get_metric",
    "search_metrics",
    "get_summary",
    "list_metric_ids",
    "get_by_category",
]

def get_metric(metric_id: str) -> Optional[MetricDefinition]:
    return _get_metric(metric_id)

def search_metrics(query: str) -> List[MetricDefinition]:
    return _search_metrics(query)

def get_summary() -> Dict[str, Any]:
    return _get_summary()

def list_metric_ids() -> List[str]:
    return sorted(METRICS.keys())

def get_by_category(category: MetricCategory) -> List[MetricDefinition]:
    return [m for m in METRICS.values() if m.category == category]