import yaml
import os

REQUIRED_BLOCKS = [
    "core", "relationships", "falsifiability",
    "benchmarks", "temporal", "aggregation", "computation"
]

class RegistryGate:
    def load_metric(self, path):
        with open(path, "r", encoding="utf-8") as f:
            metric = yaml.safe_load(f)

        missing = [b for b in REQUIRED_BLOCKS if b not in metric]
        if missing:
            raise ValueError(
                f"[REGISTRY BLOCKED] {metric.get('metric_name')} missing blocks: {missing}"
            )

        return metric

    def load_folder(self, folder):
        metrics = {}
        for file in os.listdir(folder):
            if file.endswith(".yaml"):
                full_path = os.path.join(folder, file)
                metric = self.load_metric(full_path)
                metrics[metric["metric_name"]] = metric
        return metrics