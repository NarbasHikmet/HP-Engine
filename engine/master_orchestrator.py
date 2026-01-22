from engine.registry_gate import RegistryGate
from engine.metric_engine import MetricEngine
from engine.popper_gate import PopperGate


class MasterOrchestrator:
    """
    Contract-first minimal orchestrator.
    Loads registry -> computes implemented metrics -> applies PopperGate.
    No silent drops: explicit BLOCKED reasons.
    """

    def __init__(self, registry_folder="canon/registry/tactical"):
        self.registry_folder = registry_folder
        self.gate = RegistryGate()
        self.engine = MetricEngine()
        self.popper = PopperGate()
        self.registry = self.gate.load_folder(self.registry_folder)

    def run(self, events, context=None):
        context = context or {}
        results = {
            "status": "OK",
            "context": context,
            "metrics": {},
            "blocked": {},
            "popper": None
        }

        for metric_name in self.registry.keys():
            value, reason = self._compute_metric(metric_name, events)

            if reason is None:
                results["metrics"][metric_name] = value
            else:
                results["status"] = "DEGRADED"
                results["blocked"][metric_name] = reason

        # Popper Gate (only on computed metrics)
        results["popper"] = self.popper.verify(results["metrics"])
        if results["popper"]["overall"] in ["CONFLICT", "INSUFFICIENT"]:
            results["status"] = "DEGRADED"

        return results

    def _compute_metric(self, metric_name, events):
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

            if metric_name == "Pressing_Intensity":
                value = self.engine.compute_pressing_intensity(events)
                if value is None:
                    return None, "BLOCKED: No opponent passes -> Pressing_Intensity undefined"
                return value, None

            return None, "BLOCKED: Metric in registry but not implemented in MetricEngine"

        except Exception as e:
            return None, f"BLOCKED: Runtime error while computing {metric_name}: {e}"