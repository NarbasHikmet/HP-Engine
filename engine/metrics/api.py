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
    """Safe getter (canonical access point)."""
    return _get_metric(metric_id)

def search_metrics(query: str) -> List[MetricDefinition]:
    """Search by name/alias."""
    return _search_metrics(query)

def get_summary() -> Dict[str, Any]:
    """High-level encyclopedia summary."""
    return _get_summary()

def list_metric_ids() -> List[str]:
    """All metric IDs sorted."""
    return sorted(METRICS.keys())

def get_by_category(category: MetricCategory) -> List[MetricDefinition]:
    """Return all metrics in a category."""
    return [m for m in METRICS.values() if m.category == category]