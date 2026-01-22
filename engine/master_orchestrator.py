from engine.registry_gate import RegistryGate
from engine.metric_engine import MetricEngine


class MasterOrchestrator:
    """
    Contract-first minimal orchestrator.
    - Loads registry (YAML)
    - Computes metrics that MetricEngine knows
    - Returns explicit report (no silent drops)
    """

    def __init__(self, registry_folder="canon/registry/tactical"):
        self.registry_folder = registry_folder
        self.gate = RegistryGate()
        self.engine = MetricEngine()
        self.registry = self.gate.load_folder(self.registry_folder)

    def run(self, events, context=None):
        """
        events: list[dict] (SportsBase-like normalized events)
        context: dict (optional; future: league/season/venue)
        """
        context = context or {}
        results = {
            "status": "OK",
            "context": context,
            "metrics": {},
            "blocked": {},
        }

        for metric_name in self.registry.keys():
            value, reason = self._compute_metric(metric_name, events)

            if reason is None:
                results["metrics"][metric_name] = value
            else:
                results["status"] = "DEGRADED"
                results["blocked"][metric_name] = reason

        return results

    def _compute_metric(self, metric_name, events):
        """
        Returns: (value, reason)
        - reason None => OK
        - reason str  => BLOCKED with explicit reason
        """
        try:
            if metric_name == "PPDA":
                value = self.engine.compute_ppda(events)
                if value is None:
                    return None, "BLOCKED: No defensive actions -> PPDA undefined"
                return value, None

            if metric_name == "Field_Tilt":
                value = self.engine.compute_field_tilt(events)
                if value is None:
                    return None, "BLOCKED: No final-third passes -> Field_Tilt undefined"
                return value, None

            # Metric exists in registry but engine doesn't implement it yet
            return None, "BLOCKED: Metric in registry but not implemented in MetricEngine"

        except Exception as e:
            return None, f"BLOCKED: Runtime error while computing {metric_name}: {e}"